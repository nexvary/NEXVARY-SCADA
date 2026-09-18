from nexvary_scada.models import AlarmRule, Compare, Severity, TagValue
from nexvary_scada.services.alarms import AlarmEngine


def test_alarm_raises_and_clears():
    engine = AlarmEngine([AlarmRule("hot", "temp", Compare.GT, 50, Severity.HIGH, "Too hot")])
    first = engine.evaluate([TagValue("temp", 60)])[0]
    assert first.active is True
    assert first.value == 60
    cleared = engine.evaluate([TagValue("temp", 40)])[0]
    assert cleared.active is False
