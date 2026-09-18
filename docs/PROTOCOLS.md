# Protocol support

## Ready and tested in CI

### Modbus TCP
- Coils
- Discrete inputs
- Holding registers
- Input registers
- uint16 / int16 / scaled numeric decoding
- Single-coil and single-holding-register writes
- Unit ID, timeout and per-tag mapping
- Real-hardware writes are blocked by the runtime kill-switch unless explicitly commissioned.

### Modbus RTU / RS-485
- CRC16 validation
- Coils
- Discrete inputs
- Holding registers
- Input registers
- uint16 / int16 / scaled numeric decoding
- Single-coil and single-holding-register writes
- Serial parameters: port, baud, parity, stop bits, timeout
- Requires the optional `industrial` dependency group for pyserial.

## Planned adapters

- OPC UA
- MQTT
- REST / vendor gateways

The protocol driver interface is isolated from HMI and historian layers so additional adapters can be added without changing operator screens.
