from __future__ import annotations

from datetime import datetime, timezone

from nexvary_scada.models import AlarmEvent, AlarmRule, Compare, TagValue


def _matches(comparator: Compare, value: object, threshold: object) -> bool:
    if comparator == Compare.EQ:
        return value == threshold
    if comparator == Compare.NE:
        return value != threshold
    if comparator == Compare.GT:
        return float(value) > float(threshold)
    if comparator == Compare.GTE:
        return float(value) >= float(threshold)
    if comparator == Compare.LT:
        return float(value) < float(threshold)
    if comparator == Compare.LTE:
        return float(value) <= float(threshold)
    raise ValueError(f"Unsupported comparator: {comparator}")


class AlarmEngine:
    def __init__(self, rules: list[AlarmRule]) -> None:
        self.rules = rules
        self._events: dict[str, AlarmEvent] = {}

    def evaluate(self, values: list[TagValue]) -> list[AlarmEvent]:
        by_tag = {item.tag_id: item for item in values}
        now = datetime.now(timezone.utc)
        for rule in self.rules:
            current = by_tag.get(rule.tag_id)
            if current is None:
                continue
            active = _matches(rule.comparator, current.value, rule.threshold)
            previous = self._events.get(rule.id)
            if previous is None:
                self._events[rule.id] = AlarmEvent(
                    rule_id=rule.id,
                    tag_id=rule.tag_id,
                    severity=rule.severity,
                    message=rule.message,
                    active=active,
                    value=current.value,
                    raised_at=now,
                    changed_at=now,
                )
            elif previous.active != active:
                raised_at = now if active else previous.raised_at
                self._events[rule.id] = AlarmEvent(
                    rule_id=rule.id,
                    tag_id=rule.tag_id,
                    severity=rule.severity,
                    message=rule.message,
                    active=active,
                    value=current.value,
                    raised_at=raised_at,
                    changed_at=now,
                )
            else:
                previous.value = current.value
        return self.events()

    def events(self, *, active_only: bool = False) -> list[AlarmEvent]:
        events = list(self._events.values())
        if active_only:
            events = [event for event in events if event.active]
        return sorted(events, key=lambda event: (not event.active, event.severity.value, event.rule_id))
