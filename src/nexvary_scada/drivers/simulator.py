from __future__ import annotations

import math
from dataclasses import dataclass

from nexvary_scada.drivers.base import DriverError, IndustrialDriver
from nexvary_scada.models import DeviceDefinition, TagDefinition, TagValue


@dataclass(slots=True)
class _SimState:
    tick: int = 0
    pump_run: bool = True
    pump_fault: bool = False
    emergency_stop: bool = False


class ProcessSimulator(IndustrialDriver):
    name = "Process Simulator"

    def __init__(self) -> None:
        self.device = DeviceDefinition(
            id="simulator-01",
            name="Demo Process",
            driver="simulator",
            writes_enabled=True,
            description="Built-in deterministic process simulator",
        )
        self.state = _SimState()
        self._definitions = [
            TagDefinition("pump_01_run", "Pump 01 Running", writable=True),
            TagDefinition("pump_01_fault", "Pump 01 Fault", writable=True),
            TagDefinition("emergency_stop", "Emergency Stop", writable=True),
            TagDefinition("tank_level", "Tank Level", "%"),
            TagDefinition("line_pressure", "Line Pressure", "bar"),
            TagDefinition("process_temp", "Process Temperature", "°C"),
            TagDefinition("flow_rate", "Flow Rate", "m³/h"),
        ]

    def definitions(self):
        return tuple(self._definitions)

    def _values(self) -> list[TagValue]:
        t = self.state.tick
        run = self.state.pump_run and not self.state.pump_fault and not self.state.emergency_stop
        tank_level = 58.0 + 18.0 * math.sin(t / 13.0)
        pressure = (5.1 + 1.25 * math.sin(t / 7.0)) if run else 0.35
        temperature = 61.0 + 10.0 * math.sin(t / 17.0) + (7.0 if self.state.pump_fault else 0.0)
        flow = (36.0 + 7.0 * math.sin(t / 5.0)) if run else 0.0
        return [
            TagValue("pump_01_run", run),
            TagValue("pump_01_fault", self.state.pump_fault),
            TagValue("emergency_stop", self.state.emergency_stop),
            TagValue("tank_level", round(tank_level, 2)),
            TagValue("line_pressure", round(pressure, 2)),
            TagValue("process_temp", round(temperature, 2)),
            TagValue("flow_rate", round(flow, 2)),
        ]

    def read_all(self) -> list[TagValue]:
        self.state.tick += 1
        return self._values()

    def write(self, tag_id: str, value: object) -> TagValue:
        writable = {d.id for d in self._definitions if d.writable}
        if tag_id not in writable:
            raise DriverError(f"Tag {tag_id} is read-only")
        if tag_id == "pump_01_run":
            self.state.pump_run = bool(value)
        elif tag_id == "pump_01_fault":
            self.state.pump_fault = bool(value)
        elif tag_id == "emergency_stop":
            self.state.emergency_stop = bool(value)
        return next(item for item in self._values() if item.tag_id == tag_id)
