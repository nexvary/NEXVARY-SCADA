from __future__ import annotations

import socket
import struct
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import count

from nexvary_scada.drivers.base import DriverError, DriverHealth, IndustrialDriver, WriteBlockedError
from nexvary_scada.models import DeviceDefinition, Quality, TagDefinition, TagValue

FUNCTIONS = {
    "coil": 0x01,
    "discrete_input": 0x02,
    "holding_register": 0x03,
    "input_register": 0x04,
}


@dataclass(slots=True)
class ModbusTagSpec:
    id: str
    name: str
    register: str
    address: int
    unit: str = ""
    data_type: str = "uint16"
    scale: float = 1.0
    offset: float = 0.0
    writable: bool = False
    description: str = ""

    def definition(self, device_id: str) -> TagDefinition:
        return TagDefinition(
            id=self.id,
            name=self.name,
            unit=self.unit,
            writable=self.writable,
            description=self.description,
            device_id=device_id,
            source=f"modbus:{self.register}:{self.address}",
        )


class ModbusTcpDriver(IndustrialDriver):
    name = "Modbus TCP"

    def __init__(
        self,
        *,
        device_id: str,
        name: str,
        host: str,
        port: int = 502,
        unit_id: int = 1,
        tags: Iterable[ModbusTagSpec],
        timeout: float = 2.0,
        writes_enabled: bool = False,
    ) -> None:
        self.device = DeviceDefinition(
            id=device_id,
            name=name,
            driver="modbus_tcp",
            writes_enabled=writes_enabled,
            description=f"{host}:{port} unit={unit_id}",
        )
        self.host = host
        self.port = int(port)
        self.unit_id = int(unit_id)
        self.timeout = float(timeout)
        self.tags = list(tags)
        self._transaction = count(1)
        self._last_health = DriverHealth(False, "Not polled")

    def definitions(self):
        return tuple(tag.definition(self.device.id) for tag in self.tags)

    def health(self) -> DriverHealth:
        return self._last_health

    def _exchange(self, function: int, payload: bytes) -> bytes:
        transaction = next(self._transaction) & 0xFFFF
        pdu = bytes([function]) + payload
        frame = struct.pack(">HHHB", transaction, 0, len(pdu) + 1, self.unit_id) + pdu
        try:
            with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
                sock.settimeout(self.timeout)
                sock.sendall(frame)
                header = self._recv_exact(sock, 7)
                rx_transaction, protocol, length, unit = struct.unpack(">HHHB", header)
                if protocol != 0 or unit != self.unit_id or rx_transaction != transaction:
                    raise DriverError("Invalid Modbus TCP response header")
                response = self._recv_exact(sock, length - 1)
        except (OSError, TimeoutError) as exc:
            self._last_health = DriverHealth(False, str(exc))
            raise DriverError(f"Modbus connection failed: {exc}") from exc

        if not response:
            raise DriverError("Empty Modbus response")
        response_function = response[0]
        if response_function == (function | 0x80):
            code = response[1] if len(response) > 1 else -1
            raise DriverError(f"Modbus exception {code}")
        if response_function != function:
            raise DriverError("Unexpected Modbus function in response")
        self._last_health = DriverHealth(True, "Connected")
        return response[1:]

    @staticmethod
    def _recv_exact(sock: socket.socket, length: int) -> bytes:
        chunks = bytearray()
        while len(chunks) < length:
            chunk = sock.recv(length - len(chunks))
            if not chunk:
                raise DriverError("Connection closed during Modbus response")
            chunks.extend(chunk)
        return bytes(chunks)

    def _read_raw(self, spec: ModbusTagSpec) -> bool | int:
        try:
            function = FUNCTIONS[spec.register]
        except KeyError as exc:
            raise DriverError(f"Unsupported Modbus register type: {spec.register}") from exc
        response = self._exchange(function, struct.pack(">HH", spec.address, 1))
        if spec.register in {"coil", "discrete_input"}:
            if len(response) < 2 or response[0] < 1:
                raise DriverError("Malformed Modbus bit response")
            return bool(response[1] & 0x01)
        if len(response) < 3 or response[0] < 2:
            raise DriverError("Malformed Modbus register response")
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
        values: list[TagValue] = []
        for spec in self.tags:
            try:
                value = self._decode(spec, self._read_raw(spec))
                values.append(TagValue(spec.id, value, Quality.GOOD, device_id=self.device.id))
            except DriverError:
                values.append(TagValue(spec.id, None, Quality.BAD, device_id=self.device.id))
        return values

    def write(self, tag_id: str, value: object) -> TagValue:
        if not self.device.writes_enabled:
            raise WriteBlockedError("Writes are disabled for this Modbus device")
        spec = next((tag for tag in self.tags if tag.id == tag_id), None)
        if spec is None:
            raise DriverError(f"Unknown tag: {tag_id}")
        if not spec.writable:
            raise WriteBlockedError(f"Tag {tag_id} is read-only")
        if spec.register == "coil":
            raw = 0xFF00 if bool(value) else 0x0000
            self._exchange(0x05, struct.pack(">HH", spec.address, raw))
            return TagValue(spec.id, bool(value), device_id=self.device.id)
        if spec.register == "holding_register":
            numeric = float(value)
            if spec.scale == 0:
                raise DriverError("Scale cannot be zero")
            raw = round((numeric - spec.offset) / spec.scale)
            if not 0 <= raw <= 0xFFFF:
                raise DriverError("Encoded register value is outside uint16 range")
            self._exchange(0x06, struct.pack(">HH", spec.address, raw))
            return TagValue(spec.id, numeric, device_id=self.device.id)
        raise WriteBlockedError(f"Register type {spec.register} does not support writes")
