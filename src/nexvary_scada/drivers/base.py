from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from nexvary_scada.models import TagDefinition, TagValue


class DriverError(RuntimeError):
    pass


class IndustrialDriver(ABC):
    """Minimal contract implemented by simulators and real protocol drivers."""

    name: str

    @abstractmethod
    def definitions(self) -> Iterable[TagDefinition]:
        raise NotImplementedError

    @abstractmethod
    def read_all(self) -> list[TagValue]:
        raise NotImplementedError

    def write(self, tag_id: str, value: object) -> TagValue:
        raise DriverError(f"Driver {self.name} does not permit writes")
