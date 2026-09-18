import pytest

from nexvary_scada.drivers.base import WriteBlockedError
from nexvary_scada.drivers.modbus_tcp import ModbusTagSpec, ModbusTcpDriver
from nexvary_scada.services.devices import DeviceManager
from nexvary_scada.services.runtime import ScadaRuntime


def test_viewer_cannot_write_simulator():
    runtime = ScadaRuntime()
    with pytest.raises(WriteBlockedError):
        runtime.write("pump_01_run", False, operator="viewer", role="viewer")


def test_real_writes_have_global_kill_switch(monkeypatch):
    monkeypatch.delenv("NEXVARY_SCADA_ENABLE_REAL_WRITES", raising=False)
    driver = ModbusTcpDriver(
        device_id="plc-01",
        name="PLC",
        host="127.0.0.1",
        writes_enabled=True,
        tags=[ModbusTagSpec("setpoint", "Setpoint", "holding_register", 1, writable=True)],
    )
    runtime = ScadaRuntime(manager=DeviceManager([driver]))
    with pytest.raises(WriteBlockedError, match="globally disabled"):
        runtime.write("setpoint", 5, operator="engineer", role="engineer")


def test_alarm_ack_is_audited():
    runtime = ScadaRuntime()
    runtime.poll()
    runtime.write("pump_01_fault", True, operator="operator-1", role="operator")
    event = runtime.acknowledge_alarm("pump-fault", operator="operator-1", role="operator")
    assert event.acknowledged is True
    assert runtime.audit.recent()[0]["action"] == "alarm.ack"
