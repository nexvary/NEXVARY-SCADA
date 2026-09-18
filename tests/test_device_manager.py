import json

from nexvary_scada.services.devices import DeviceManager


def test_device_manager_loads_json(tmp_path):
    config = {
        "include_simulator": True,
        "devices": [{
            "id": "plc-01",
            "name": "PLC 01",
            "driver": "modbus_tcp",
            "host": "127.0.0.1",
            "tags": [{"id": "x", "name": "X", "register": "holding_register", "address": 0}],
        }],
    }
    path = tmp_path / "devices.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    manager = DeviceManager.from_json(path)
    ids = {item["id"] for item in manager.devices()}
    assert ids == {"simulator-01", "plc-01"}
