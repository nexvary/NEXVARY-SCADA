from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from nexvary_scada.drivers.base import DriverError, IndustrialDriver
from nexvary_scada.drivers.modbus_rtu import ModbusRtuDriver
from nexvary_scada.drivers.modbus_tcp import ModbusTagSpec, ModbusTcpDriver
from nexvary_scada.drivers.simulator import ProcessSimulator
from nexvary_scada.models import TagDefinition, TagValue


class DeviceManager:
    def __init__(self, drivers: list[IndustrialDriver] | None = None) -> None:
        self._drivers: dict[str, IndustrialDriver] = {}
        for driver in drivers or [ProcessSimulator()]:
            self.add(driver)

    def add(self, driver: IndustrialDriver) -> None:
        if driver.device.id in self._drivers:
            raise ValueError(f"Duplicate device id: {driver.device.id}")
        existing_tags = {tag.id for item in self._drivers.values() for tag in item.definitions()}
        incoming_tags = {tag.id for tag in driver.definitions()}
        duplicates = existing_tags & incoming_tags
        if duplicates:
            raise ValueError(f"Duplicate tag ids across devices: {sorted(duplicates)}")
        self._drivers[driver.device.id] = driver

    def devices(self) -> list[dict]:
        result = []
        for driver in self._drivers.values():
            health = driver.health()
            result.append({
                **asdict(driver.device),
                "health": asdict(health),
                "tag_count": len(tuple(driver.definitions())),
            })
        return result

    def definitions(self) -> list[TagDefinition]:
        return [tag for driver in self._drivers.values() for tag in driver.definitions()]

    def driver_for_tag(self, tag_id: str) -> IndustrialDriver:
        for driver in self._drivers.values():
            if any(tag.id == tag_id for tag in driver.definitions()):
                return driver
        raise DriverError(f"Unknown tag: {tag_id}")

    def read_all(self) -> list[TagValue]:
        values: list[TagValue] = []
        for driver in self._drivers.values():
            if driver.device.enabled:
                values.extend(driver.read_all())
        return values

    def write(self, tag_id: str, value: object) -> TagValue:
        return self.driver_for_tag(tag_id).write(tag_id, value)

    @classmethod
    def from_json(cls, path: str | Path) -> DeviceManager:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        drivers: list[IndustrialDriver] = []
        if payload.get("include_simulator", True):
            drivers.append(ProcessSimulator())
        for item in payload.get("devices", []):
            tags = [ModbusTagSpec(**tag) for tag in item.get("tags", [])]
            if item.get("driver") == "modbus_tcp":
                drivers.append(ModbusTcpDriver(
                    device_id=item["id"], name=item.get("name", item["id"]), host=item["host"],
                    port=item.get("port", 502), unit_id=item.get("unit_id", 1),
                    timeout=item.get("timeout", 2.0), writes_enabled=item.get("writes_enabled", False), tags=tags,
                ))
            elif item.get("driver") == "modbus_rtu":
                drivers.append(ModbusRtuDriver(
                    device_id=item["id"], name=item.get("name", item["id"]), port=item["port"],
                    unit_id=item.get("unit_id", 1), baudrate=item.get("baudrate", 9600),
                    parity=item.get("parity", "N"), stopbits=item.get("stopbits", 1),
                    timeout=item.get("timeout", 1.0), writes_enabled=item.get("writes_enabled", False), tags=tags,
                ))
        return cls(drivers)
