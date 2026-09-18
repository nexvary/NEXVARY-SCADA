# Milestone 150 — Release baseline

This document defines the project's internal milestone numbering. The numbers are grouped engineering gates rather than one commit per number.

## Stages 1–30 — Foundation — COMPLETE

- Python package and runtime
- FastAPI local service
- deterministic process simulator
- tag model with quality and timestamps
- SQLite historian
- alarm rules and state transitions
- automated tests

## Stages 31–60 — Industrial connectivity — COMPLETE

- protocol-driver abstraction
- device registry
- JSON device configuration
- Modbus TCP reads for coils, discrete inputs, holding registers and input registers
- Modbus TCP single-coil / single-register writes
- scaling, offset and int16 support
- Modbus RTU / RS-485 CRC16 implementation
- serial settings and optional pyserial transport
- Modbus RTU integration tests using a deterministic fake transport
- example TCP and RTU configurations

## Stages 61–90 — Operations and safety controls — COMPLETE

- multi-device runtime
- device health surface
- duplicate tag protection
- historian time windows and sample counts
- alarm acknowledgement
- operator audit trail
- viewer/operator/engineer/admin action gating
- per-device write permission
- independent global hardware-write kill-switch
- simulator-only compatibility path
- nuclear scope boundary documented as non-safety monitoring/simulation/training/maintenance only

## Stages 91–120 — HMI and operator experience — COMPLETE

- distinct Overview, HMI, Devices, Alarms, Historian, Audit, Settings and About pages
- live process mimic
- live tag table with quality/source/device
- device health cards
- alarm console with acknowledgement
- native trend canvas using historian data
- operator identity/role local session controls
- responsive phone/tablet layout
- Arabic RTL support
- navigation labels for Arabic, English, Turkish, Spanish, German, Italian, French, Urdu, Persian and Russian
- NEXVARY About/social contact surface

## Stages 121–150 — Verification and packaging — COMPLETE when gates are green

- Python 3.11 / 3.12 / 3.13 CI matrix
- compile check
- unit/integration tests
- Ruff static checks
- Bandit static security scan
- explicit Release Gate job
- PyInstaller application packaging
- Windows x64 executable build
- Ubuntu x64 executable build
- executable-level smoke check
- build artifacts uploaded by GitHub Actions

## Post-150 backlog

These are intentionally not represented as completed:

- OPC UA adapter
- MQTT adapter
- graphical drag/drop HMI designer
- TLS termination / production identity provider integration
- PostgreSQL/Timescale historian backend
- high-availability runtime
- Android monitoring client
- signed Windows installer
- hardware-in-the-loop commissioning against named PLC/RTU models

The general-purpose NEXVARY SCADA product does not implement nuclear safety-class I&C, reactor protection, SCRAM or engineered safety actuation logic.
