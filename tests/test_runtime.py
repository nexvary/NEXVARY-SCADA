from nexvary_scada.services.runtime import ScadaRuntime


def test_runtime_polls_all_demo_tags():
    runtime = ScadaRuntime()
    values = runtime.poll()
    ids = {item.tag_id for item in values}
    assert {"tank_level", "line_pressure", "process_temp", "flow_rate"}.issubset(ids)


def test_simulator_fault_activates_alarm():
    runtime = ScadaRuntime()
    runtime.poll()
    runtime.write_simulated("pump_01_fault", True)
    active = {event.rule_id for event in runtime.alarms.events(active_only=True)}
    assert "pump-fault" in active
