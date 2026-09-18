# NEXVARY SCADA Architecture

## Runtime path

Field or simulated device -> Protocol Driver -> Tag Model -> Alarm Engine -> Historian -> API -> HMI.

The runtime deliberately keeps protocol drivers behind a small interface so Modbus TCP/RTU, OPC UA and MQTT adapters can be added without coupling the HMI to vendor-specific libraries.

## Write policy

Version 0.1 enables writes only against the built-in simulator. Real industrial write operations will require an explicit driver capability, role authorization, audit logging and per-tag allowlisting.

## Power and nuclear profile

The architecture may represent conventional generation and non-safety nuclear auxiliary/monitoring data. Nuclear safety-class instrumentation and control, reactor protection, engineered safety features actuation, SCRAM logic and other safety-critical control functions are excluded from this general-purpose platform.
