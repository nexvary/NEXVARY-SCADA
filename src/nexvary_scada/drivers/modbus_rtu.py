from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import Protocol

from nexvary_scada.drivers.base import DriverError, DriverHealth, IndustrialDriver, WriteBlockedError
from nexvary_scada.drivers.modbus_tcp import FUNCTIONS, ModbusTagSpec
from nexvary_scada.models import DeviceDefinition, Quality, TagValue


def crc16_modbus(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc & 0xFFFF


def append_crc(data: bytes) -> bytes:
    return data + struct.pack("<H", crc16_modbus(data))


class RtuTransport(Protocol):
    def request(self, frame: bytes, expected_length: int) -> bytes: ...


@dataclass(slots=True)
class SerialRtuTransport:
    port: str
    baudrate: int = 9600
    bytesize: int = 8
    parity: str = "N"
    stopbits: int = 1
    timeout: float = 1.0

    def request(self, frame: bytes, expected_length: int) -> bytes:
        try:
            import serial
        except ImportError as exc:
            raise DriverError('pyserial is required for Modbus RTU. Install ".[industrial]"') from exc
        try:
            with serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
                timeout=self.timeout,
            ) as connection:
                connection.reset_input_buffer()
                connection.write(frame)
                connection.flush()
                response = connection.read(expected_length)
        except Exception as exc:
            raise DriverError(f"Modbus RTU serial error: {exc}") from exc
        if len(response) != expected_length:
            raise DriverError(f"Short Modbus RTU response: expected {expected_length}, got {len(response)}")
        return response


class ModbusRtuDriver(IndustrialDriver):
    name = "Modbus RTU"

    def __init__(
        self,
        *,
        device_id: str,
        name: str,
        port: str,
        unit_id: int = 1,
        tags: list[ModbusTagSpec],
        baudrate: int = 9600,
        parity: str = "N",
        stopbits: int = 1,
        timeout: float = 1.0,
        writes_enabled: bool = False,
        transport: RtuTransport | None = None,
    ) -> None:
        self.device = DeviceDefinition(
            id=device_id,
            name=name,
            driver="modbus_rtu",
            writes_enabled=writes_enabled,
            description=f"{port} {baudrate}bps unit={unit_id}",
        )
        self.port = port
        self.unit_id = int(unit_id)
        self.tags = list(tags)
        self.transport = transport or SerialRtuTransport(
            port=port, baudrate=baudrate, parity=parity, stopbits=stopbits, timeout=timeout
        )
        self._last_health = DriverHealth(False, "Not polled")

    def definitions(self):
        return tuple(tag.definition(self.device.id) for tag in self.tags)

    def health(self) -> DriverHealth:
        return self._last_health

    def _exchange(self, function: int, payload: bytes, expected_length: int) -> bytes:
        request = append_crc(bytes([self.unit_id, function]) + payload)
        try:
            response = self.transport.request(request, expected_length)
        except DriverError as exc:
            self._last_health = DriverHealth(False, str(exc))
            raise
        if len(response) < 5:
            raise DriverError("Malformed Modbus RTU response")
        body, received_crc = response[:-2], struct.unpack("<H", response[-2:])[0]
        if crc16_modbus(body) != received_crc:
            raise DriverError("Modbus RTU CRC mismatch")
        if body[0] != self.unit_id:
            raise DriverError("Unexpected Modbus RTU unit id")
        response_function = body[1]
        if response_function == (function | 0x80):
            code = body[2] if len(body) > 2 else -1
            raise DriverError(f"Modbus exception {code}")
        if response_function != function:
            raise DriverError("Unexpected Modbus RTU function")
        self._last_health = DriverHealth(True, "Connected")
        return body[2:]

    def _read_raw(self, spec: ModbusTagSpec) -> bool | int:
        try:
            function = FUNCTIONS[spec.register]
        except KeyError as exc:
            raise DriverError(f"Unsupported Modbus register type: {spec.register}") from exc
        expected = 6 if spec.register in {"coil", "discrete_input"} else 7
        response = self._exchange(function, struct.pack(">HH", spec.address, 1), expected)
        if spec.register in {"coil", "discrete_input"}:
            if len(response) < 2 or response[0] < 1:
                raise DriverError("Malformed Modbus RTU bit response")
            return bool(response[1] & 0x01)
        if len(response) < 3 or response[0] < 2:
            raise DriverError("Malformed Modbus RTU register response")
        raw = struct.unpack(">H", response[1:3])[0]
        if spec.data_type == "int16":
            raw = struct.unpack(">h", struct.pack(">H", raw))[0]
        elif spec.data_type not in {"uint16", "float_scaled"}:
            raise DriverError(f"Unsupported data type: {spec.data_type}")
        return raw

    @staticmethod
    def _decode(spec: ModbusTagSpec, raw: bool | int) -> bool | int | float:
        if isinstance(raw, bool):
            return raw
        value = raw * spec.scale + spec.offset
        if spec.scale == 1.0 and spec.offset == 0.0 and spec.data_type != "float_scaled":
            return int(value)
        return round(float(value), 6)

    def read_all(self) -> list[TagValue]:
        values=[]
        for spec in self.tags:
            try:
                values.append(TagValue(spec.id, self._decode(spec, self._read_raw(spec)), Quality.GOOD, device_id=self.device.id))
            except DriverError:
                values.append(TagValue(spec.id, None, Quality.BAD, device_id=self.device.id))
        return values

    def write(self, tag_id: str, value: object) -> TagValue:
        if not self.device.writes_enabled:
            raise WriteBlockedError("Writes are disabled for this Modbus RTU device")
        spec = next((tag for tag in self.tags if tag.id == tag_id), None)
        if spec is None:
            raise DriverError(f"Unknown tag: {tag_id}")
        if not spec.writable:
            raise WriteBlockedError(f"Tag {tag_id} is read-only")
        if spec.register == "coil":
            raw = 0xFF00 if bool(value) else 0x0000
            self._exchange(0x05, struct.pack(">HH", spec.address, raw), 8)
            return TagValue(spec.id, bool(value), device_id=self.device.id)
        if spec.register == "holding_register":
            if spec.scale == 0:
                raise DriverError("Scale cannot be zero")
            raw = round((float(value) - spec.offset) / spec.scale)
            if not 0 <= raw <= 0xFFFF:
                raise DriverError("Encoded register value is outside uint16 range")
            self._exchange(0x06, struct.pack(">HH", spec.address, raw), 8)
            return TagValue(spec.id, float(value), device_id=self.device.id)
        raise WriteBlockedError(f"Register type {spec.register} does not support writes")
