import struct

from nexvary_scada.drivers.modbus_rtu import ModbusRtuDriver, append_crc, crc16_modbus
from nexvary_scada.drivers.modbus_tcp import ModbusTagSpec


class FakeTransport:
    def request(self, frame: bytes, expected_length: int) -> bytes:
        assert crc16_modbus(frame[:-2]) == struct.unpack("<H", frame[-2:])[0]
        unit, function = frame[0], frame[1]
        address = struct.unpack(">H", frame[2:4])[0]
        if function == 0x04:
            value = 2315 if address == 2 else 0
            return append_crc(bytes([unit, function, 2]) + struct.pack(">H", value))
        if function == 0x01:
            return append_crc(bytes([unit, function, 1, 1]))
        raise AssertionError(function)


def test_crc_known_vector():
    payload = bytes.fromhex("01030000000A")
    assert crc16_modbus(payload) == 0xCDC5


def test_rtu_reads_scaled_register_and_coil():
    driver = ModbusRtuDriver(
        device_id="rtu-1", name="RTU", port="TEST", unit_id=1, transport=FakeTransport(),
        tags=[
            ModbusTagSpec("voltage", "Voltage", "input_register", 2, scale=0.1, data_type="float_scaled"),
            ModbusTagSpec("run", "Run", "coil", 1),
        ],
    )
    values = {item.tag_id:item for item in driver.read_all()}
    assert values["voltage"].value == 231.5
    assert values["run"].value is True
    assert driver.health().connected is True
