# NEXVARY SCADA

Industrial Monitoring & Control Platform

NEXVARY SCADA is a cross-platform industrial operations platform focused on HMI/SCADA monitoring, alarms, historian data, protocol integration, simulation, maintenance workflows, and operator visibility.

## Current functional baseline

- Device and tag model
- Process / PLC simulator
- Alarm engine with severity and active/clear state
- SQLite historian
- FastAPI runtime
- Responsive dark / Royal Gold HMI
- Process mimic for tank, pump and process line
- Simulator-only Start/Stop, Fault and E-Stop controls
- Automated tests and GitHub Actions CI
- Driver abstraction prepared for Modbus, OPC UA and MQTT

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

Open:

```text
http://127.0.0.1:8765
```

Run tests:

```bash
pytest -q
```

## Planned protocol layer

- Modbus TCP
- Modbus RTU / RS-485
- OPC UA
- MQTT
- REST / vendor gateways

Real industrial write operations will require explicit driver capability, role authorization, audit logging and per-tag allowlisting.

## Power-generation scope

The platform architecture can represent conventional power-generation systems and non-safety nuclear auxiliary/monitoring data.

> Nuclear scope is intentionally limited to non-safety monitoring, simulation, training, historian, maintenance and auxiliary systems. Reactor protection, safety-class I&C, SCRAM and other safety-critical control functions are outside the product scope.
