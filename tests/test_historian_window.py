from nexvary_scada.models import TagValue
from nexvary_scada.services.historian import Historian


def test_historian_window_returns_chronological_samples():
    historian = Historian()
    historian.record([TagValue("temp", 10), TagValue("temp", 11)])
    rows = historian.window("temp", minutes=5)
    assert [row["value"] for row in rows] == [10, 11]
    assert historian.count() == 2
