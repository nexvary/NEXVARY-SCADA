from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from nexvary_scada.models import DeviceDefinition, TagDefinition, TagValue


class DriverError(RuntimeError):
    pass


class WriteBlockedError(DriverError):
    pass


@dataclass(slots=True)
class DriverHealth:
    connected: bool
    detail: str = "OK"


class IndustrialDriver(ABC):
    name: str
    device: DeviceDefinition

    @abstractmethod
    def definitions(self) -> Iterable[TagDefinition]:
        raise NotImplementedError

    @abstractmethod
    def read_all(self) -> list[TagValue]:
        raise NotImplementedError

    def health(self) -> DriverHealth:
        return DriverHealth(True, "OK")

    def write(self, tag_id: str, value: object) -> TagValue:
        raise WriteBlockedError(f"Driver {self.name} does not permit writes")
