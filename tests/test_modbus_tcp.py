import socket
import struct
import threading

from nexvary_scada.drivers.modbus_tcp import ModbusTagSpec, ModbusTcpDriver


class FakeModbusServer:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen()
        self.port = self.sock.getsockname()[1]
        self.thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self.thread.start()
        return self

    def close(self):
        self.sock.close()

    def _run(self):
        while True:
            try:
                conn, _ = self.sock.accept()
            except OSError:
                return
            with conn:
                header = conn.recv(7)
                if len(header) < 7:
                    continue
                transaction, _, length, unit = struct.unpack(">HHHB", header)
                pdu = conn.recv(length - 1)
                function = pdu[0]
                address = struct.unpack(">H", pdu[1:3])[0]
                if function == 0x03:
                    value = 725 if address == 10 else 0
                    response_pdu = bytes([0x03, 0x02]) + struct.pack(">H", value)
                elif function == 0x01:
                    response_pdu = bytes([0x01, 0x01, 0x01])
                else:
                    response_pdu = bytes([function | 0x80, 0x01])
                response = struct.pack(">HHHB", transaction, 0, len(response_pdu) + 1, unit) + response_pdu
                conn.sendall(response)


def test_modbus_tcp_reads_scaled_register_and_coil():
    server = FakeModbusServer().start()
    try:
        driver = ModbusTcpDriver(
            device_id="plc-test",
            name="PLC Test",
            host="127.0.0.1",
            port=server.port,
            unit_id=1,
            tags=[
                ModbusTagSpec("temp", "Temperature", "holding_register", 10, scale=0.1, data_type="float_scaled"),
                ModbusTagSpec("run", "Running", "coil", 3),
            ],
        )
        values = {item.tag_id: item for item in driver.read_all()}
        assert values["temp"].value == 72.5
        assert values["temp"].quality.value == "GOOD"
        assert values["run"].value is True
    finally:
        server.close()
