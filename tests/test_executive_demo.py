from nexvary_scada.services.executive import ExecutiveDemo


def test_executive_demo_is_explicitly_simulated():
    demo = ExecutiveDemo()
    snapshot = demo.snapshot()
    assert snapshot["mode"] == "SIMULATION"
    assert snapshot["classification"] == "EXECUTIVE_DEMO_DATA"
    assert snapshot["headline"]["connected_sites"] > 0
    assert snapshot["headline"]["critical_open_alarms"] == 0
    assert any(item["id"] == "nuclear" for item in snapshot["sectors"])


def test_nuclear_demo_is_non_safety_balance_of_plant_only():
    demo = ExecutiveDemo()
    snapshot = demo.nuclear_snapshot()
    assert snapshot["mode"] == "SIMULATION"
    assert snapshot["classification"] == "NON_SAFETY_BALANCE_OF_PLANT_DEMO"
    assert len(snapshot["units"]) == 4
    assert len(snapshot["systems"]) == 6
    assert len(snapshot["trend"]) == 24
    notice = snapshot["scope_notice"].lower()
    assert "reactor protection" in notice
    assert "scram" in notice
