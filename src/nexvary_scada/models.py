from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


def utcnow() -> datetime:
    return datetime.now(UTC)


class Quality(str, Enum):
    GOOD = "GOOD"
    UNCERTAIN = "UNCERTAIN"
    BAD = "BAD"


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Compare(str, Enum):
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    EQ = "eq"
    NE = "ne"


@dataclass(slots=True)
class TagDefinition:
    id: str
    name: str
    unit: str = ""
    writable: bool = False
    description: str = ""
    device_id: str = "simulator-01"
    source: str = "simulation"


@dataclass(slots=True)
class TagValue:
    tag_id: str
    value: Any
    quality: Quality = Quality.GOOD
    timestamp: datetime = field(default_factory=utcnow)
    device_id: str = "simulator-01"


@dataclass(slots=True)
class DeviceDefinition:
    id: str
    name: str
    driver: str
    enabled: bool = True
    writes_enabled: bool = False
    description: str = ""


@dataclass(slots=True)
class AlarmRule:
    id: str
    tag_id: str
    comparator: Compare
    threshold: Any
    severity: Severity
    message: str


@dataclass(slots=True)
class AlarmEvent:
    rule_id: str
    tag_id: str
    severity: Severity
    message: str
    active: bool
    value: Any
    raised_at: datetime
    changed_at: datetime
    acknowledged: bool = False
    acknowledged_by: str | None = None
    acknowledged_at: datetime | None = None
