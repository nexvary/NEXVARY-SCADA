from pathlib import Path


UI = Path("src/nexvary_scada/ui")


def test_ui_has_distinct_connected_pages_and_rtl_locales():
    html = (UI / "index.html").read_text(encoding="utf-8")
    js = (UI / "app.js").read_text(encoding="utf-8")
    for page in ("overview", "hmi", "devices", "alarms", "historian", "audit", "settings", "about"):
        assert f'id="page-{page}"' in html
        assert f'data-page="{page}"' in html
    assert '["ar","ur","fa"]' in js
    assert "/api/devices" in js
    assert "/api/audit" in js
    assert "/api/alarms/" in js
