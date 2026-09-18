from __future__ import annotations

from pathlib import Path

from nexvary_scada.drivers.base import IndustrialDriver
from nexvary_scada.drivers.simulator import ProcessSimulator
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
    def __init__(self, driver: IndustrialDriver | None = None, database: str | Path = ":memory:") -> None:
        self.driver = driver or ProcessSimulator()
        self.historian = Historian(database)
        self.alarms = AlarmEngine(DEFAULT_RULES)
        self.last_values: list[TagValue] = []

    def poll(self) -> list[TagValue]:
        values = self.driver.read_all()
        self.last_values = values
        self.historian.record(values)
        self.alarms.evaluate(values)
        return values

    def write_simulated(self, tag_id: str, value: object) -> TagValue:
        result = self.driver.write(tag_id, value)
        self.poll()
        return result
