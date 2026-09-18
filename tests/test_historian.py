from nexvary_scada.models import TagValue
from nexvary_scada.services.historian import Historian


def test_historian_round_trip():
    historian = Historian()
    historian.record([TagValue("pressure", 5.25)])
    rows = historian.latest("pressure")
    assert len(rows) == 1
    assert rows[0]["value"] == 5.25
    assert rows[0]["quality"] == "GOOD"
