from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


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


@dataclass(slots=True)
class TagValue:
    tag_id: str
    value: Any
    quality: Quality = Quality.GOOD
    timestamp: datetime = field(default_factory=utcnow)


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
