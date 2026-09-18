from __future__ import annotations

import os
from pathlib import Path

from nexvary_scada.drivers.base import DriverError, WriteBlockedError
from nexvary_scada.services.audit import AuditLog
from nexvary_scada.services.devices import DeviceManager
from nexvary_scada.models import AlarmRule, Compare, Severity, TagValue
from nexvary_scada.services.alarms import AlarmEngine
from nexvary_scada.services.historian import Historian


DEFAULT_RULES = [
    AlarmRule("pump-fault", "pump_01_fault", Compare.EQ, True, Severity.CRITICAL, "Pump 01 fault detected"),
    AlarmRule("e-stop", "emergency_stop", Compare.EQ, True, Severity.CRITICAL, "Emergency stop is active"),
    AlarmRule("tank-low", "tank_level", Compare.LT, 20, Severity.HIGH, "Tank level below 20%"),
    AlarmRule("pressure-high", "line_pressure", Compare.GT, 6.0, Severity.WARNING, "Line pressure above 6.0 bar"),
    AlarmRule("temperature-high", "process_temp", Compare.GT, 75, Severity.HIGH, "Process temperature above 75 °C"),
]


class ScadaRuntime:
    def __init__(
        self,
        manager: DeviceManager | None = None,
        database: str | Path = ":memory:",
        audit_database: str | Path | None = None,
    ) -> None:
        config = os.getenv("NEXVARY_SCADA_DEVICES")
        self.manager = manager or (DeviceManager.from_json(config) if config else DeviceManager())
        self.historian = Historian(database)
        self.audit = AuditLog(audit_database if audit_database is not None else database)
        self.alarms = AlarmEngine(DEFAULT_RULES)
        self.last_values: list[TagValue] = []

    def poll(self) -> list[TagValue]:
        values = self.manager.read_all()
        self.last_values = values
        self.historian.record(values)
        self.alarms.evaluate(values)
        return values

    def write(self, tag_id: str, value: object, *, operator: str, role: str) -> TagValue:
        if role not in {"operator", "engineer", "admin"}:
            self.audit.record(
                operator=operator, role=role, action="tag.write", target=tag_id, success=False,
                detail={"reason": "role denied"},
            )
            raise WriteBlockedError("Operator role does not permit writes")
        driver = self.manager.driver_for_tag(tag_id)
        if driver.device.driver != "simulator" and os.getenv("NEXVARY_SCADA_ENABLE_REAL_WRITES") != "1":
            self.audit.record(
                operator=operator, role=role, action="tag.write", target=tag_id, success=False,
                detail={"reason": "hardware kill-switch disabled", "device_id": driver.device.id},
            )
            raise WriteBlockedError(
                "Real device writes are globally disabled. Set NEXVARY_SCADA_ENABLE_REAL_WRITES=1 only after commissioning."
            )
        try:
            result = self.manager.write(tag_id, value)
        except DriverError as exc:
            self.audit.record(
                operator=operator, role=role, action="tag.write", target=tag_id, success=False,
                detail={"reason": str(exc), "device_id": driver.device.id},
            )
            raise
        self.audit.record(
            operator=operator, role=role, action="tag.write", target=tag_id, success=True,
            detail={"value": value, "device_id": driver.device.id},
        )
        self.poll()
        return result

    def write_simulated(self, tag_id: str, value: object) -> TagValue:
        """Backward-compatible simulator write used by tests and local demo tooling."""
        driver = self.manager.driver_for_tag(tag_id)
        if driver.device.driver != "simulator":
            raise WriteBlockedError("write_simulated can only target the built-in simulator")
        return self.write(tag_id, value, operator="local-simulator", role="operator")

    def acknowledge_alarm(self, rule_id: str, *, operator: str, role: str):
        if role not in {"operator", "engineer", "admin"}:
            raise WriteBlockedError("Operator role does not permit alarm acknowledgement")
        event = self.alarms.acknowledge(rule_id, operator)
        self.audit.record(
            operator=operator, role=role, action="alarm.ack", target=rule_id, success=True,
            detail={"tag_id": event.tag_id},
        )
        return event
