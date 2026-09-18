from pathlib import Path

UI = Path("src/nexvary_scada/ui")


def test_ui_has_distinct_connected_pages_and_rtl_locales():
    html = (UI / "index.html").read_text(encoding="utf-8")
    js = (UI / "app.js").read_text(encoding="utf-8")
    for page in ("executive", "nuclear", "overview", "hmi", "devices", "alarms", "historian", "audit", "settings", "about-us", "system-info"):
        assert f'id="page-{page}"' in html
        assert f'data-page="{page}"' in html
    assert '["ar","ur","fa"]' in js
    assert "/api/devices" in js
    assert "/api/audit" in js
    assert "/api/alarms/" in js


def test_about_us_contains_official_nexvary_channels():
    html = (UI / "index.html").read_text(encoding="utf-8")
    for value in (
        "https://nexvary.com/",
        "https://www.facebook.com/share/14p9krEn5ij/",
        "mailto:info@nexvary.com",
        "https://www.youtube.com/@NexvaryInc",
        "https://x.com/Nexvary",
    ):
        assert value in html


def test_ui_contains_vector_icon_system_and_system_information_page():
    html = (UI / "index.html").read_text(encoding="utf-8")
    for icon_id in ("i-overview", "i-hmi", "i-devices", "i-alarms", "i-historian", "i-audit", "i-settings", "i-about-us", "i-system-info"):
        assert f'id="{icon_id}"' in html
    assert "Modbus TCP" in html
    assert "Modbus RTU/RS-485" in html
    assert "Milestone 150" in html
    assert "Nuclear safety boundary" in html


def test_executive_and_nuclear_demo_surfaces_are_connected():
    html = (UI / "index.html").read_text(encoding="utf-8")
    js = (UI / "app.js").read_text(encoding="utf-8")
    assert 'SIMULATION / DEMO DATA' in html
    assert 'SIMULATION ONLY' in html
    assert '/api/executive' in js
    assert '/api/nuclear' in js
    assert 'id="nuclear-trend"' in html
