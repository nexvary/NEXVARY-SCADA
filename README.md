# NEXVARY SCADA

**Industrial Monitoring & Control Platform**

NEXVARY SCADA is a cross-platform industrial operations platform for HMI/SCADA monitoring, alarms, historian data, protocol integration, simulation, maintenance workflows and operator visibility.

## Milestone 150 baseline

- Built-in deterministic PLC/process simulator
- Multi-device registry and tag mapping
- Modbus TCP
- Modbus RTU / RS-485
- Alarm engine with acknowledgement
- SQLite historian and trends
- Audit trail
- Role-based action gating
- Per-device write policy plus a global real-hardware write kill-switch
- Responsive dark / Royal Gold HMI
- Arabic RTL plus multilingual navigation
- Windows and Ubuntu executable packaging through GitHub Actions
- CI matrix, static analysis and Release Gate

See `docs/MILESTONE_150.md` for the exact completion boundary.

## Run locally

Python 3.11+ is required.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
nexvary-scada
```

### Linux / Ubuntu

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
nexvary-scada
```

Open `http://127.0.0.1:8765`.

## Connect a Modbus device

Copy one of the examples under `config/` and set:

### Windows PowerShell

```powershell
$env:NEXVARY_SCADA_DEVICES="config/devices.example.json"
nexvary-scada
```

For RTU/RS-485 install the optional serial dependency:

```powershell
python -m pip install -e ".[industrial]"
```

Real hardware writes are blocked by default even when a device mapping marks a tag writable. Commissioning requires both the device-level setting and the explicit server environment kill-switch.

## Verification

```bash
pytest -q
ruff check src tests packaging
bandit -q -r src
```

GitHub Actions also builds and smoke-tests Windows and Ubuntu executables.

## Protocol status

Ready:
- Modbus TCP
- Modbus RTU / RS-485

Post-150:
- OPC UA
- MQTT
- REST/vendor gateways

## Power-generation scope

The architecture can represent conventional generation and **non-safety** nuclear auxiliary/monitoring data.

> Nuclear scope is intentionally limited to non-safety monitoring, simulation, training, historian, maintenance and auxiliary systems. Reactor protection, safety-class I&C, SCRAM and other safety-critical control functions are outside the product scope.
