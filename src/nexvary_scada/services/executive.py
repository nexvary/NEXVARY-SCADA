from __future__ import annotations

import math
from datetime import UTC, datetime


class ExecutiveDemo:
    """Deterministic presentation data.

    This service intentionally models executive/demo information only. Nuclear
    values are limited to non-safety balance-of-plant and grid-facing systems.
    """

    def __init__(self) -> None:
        self._tick = 0

    def _wave(self, center: float, amplitude: float, divisor: float) -> float:
        return center + amplitude * math.sin(self._tick / divisor)

    def snapshot(self) -> dict:
        self._tick += 1
        total_generation = round(self._wave(6870.0, 95.0, 8.0), 1)
        monitored_assets = 148
        healthy_assets = 145
        return {
            "mode": "SIMULATION",
            "classification": "EXECUTIVE_DEMO_DATA",
            "timestamp": datetime.now(UTC).isoformat(),
            "headline": {
                "connected_sites": 7,
                "monitored_assets": monitored_assets,
                "asset_health_percent": round(healthy_assets / monitored_assets * 100, 1),
                "generation_mw": total_generation,
                "critical_open_alarms": 0,
                "audit_coverage_percent": 100.0,
            },
            "sectors": [
                {"id": "generation", "name": "Power Generation", "sites": 2, "status": "HEALTHY", "accent": "gold"},
                {"id": "nuclear", "name": "Nuclear Power — Non-Safety", "sites": 1, "status": "SIMULATION", "accent": "purple"},
                {"id": "water", "name": "Water & Utilities", "sites": 1, "status": "HEALTHY", "accent": "blue"},
                {"id": "oil-gas", "name": "Oil & Gas", "sites": 1, "status": "HEALTHY", "accent": "amber"},
                {"id": "manufacturing", "name": "Manufacturing", "sites": 1, "status": "HEALTHY", "accent": "green"},
                {"id": "infrastructure", "name": "Critical Infrastructure", "sites": 1, "status": "MONITORED", "accent": "cyan"},
            ],
            "capabilities": [
                "Unified multi-site operations view",
                "Modbus TCP and Modbus RTU / RS-485 integration",
                "Historian, trends and alarm management",
                "Operator roles and immutable-style audit trail",
                "Arabic RTL and multilingual HMI",
                "Local Windows / Ubuntu deployment",
                "Real-hardware write kill-switch",
                "Executive and technical operating views",
            ],
        }

    def nuclear_snapshot(self) -> dict:
        self._tick += 1
        unit_base = [1118.0, 1109.0, 1096.0, 1112.0]
        units = []
        for index, base in enumerate(unit_base, start=1):
            load = round(base + 7.0 * math.sin((self._tick + index) / 7.0), 1)
            units.append(
                {
                    "unit": index,
                    "status": "SIMULATED ONLINE",
                    "generator_load_mw": load,
                    "turbine_speed_rpm": 3000,
                    "availability_percent": round(98.2 + 0.35 * math.sin((self._tick + index) / 9.0), 1),
                }
            )

        total = round(sum(unit["generator_load_mw"] for unit in units), 1)
        return {
            "mode": "SIMULATION",
            "classification": "NON_SAFETY_BALANCE_OF_PLANT_DEMO",
            "timestamp": datetime.now(UTC).isoformat(),
            "plant": "NEXVARY Nuclear Demonstration Plant",
            "units": units,
            "headline": {
                "gross_generation_mw": total,
                "grid_frequency_hz": round(self._wave(50.0, 0.018, 4.0), 3),
                "auxiliary_load_mw": round(self._wave(205.0, 5.5, 8.0), 1),
                "cooling_water_inlet_c": round(self._wave(27.2, 0.8, 11.0), 1),
                "systems_available": "6 / 6",
                "open_critical_alarms": 0,
            },
            "systems": [
                {"name": "Turbine & Generator", "status": "AVAILABLE", "detail": f"{total:.1f} MW gross"},
                {"name": "Main Condenser", "status": "AVAILABLE", "detail": "Vacuum stable · simulated"},
                {"name": "Feedwater System", "status": "AVAILABLE", "detail": "Secondary-side monitoring"},
                {"name": "Cooling Water", "status": "AVAILABLE", "detail": "Pumps and temperatures monitored"},
                {"name": "Auxiliary Electrical", "status": "AVAILABLE", "detail": "Plant auxiliary load monitored"},
                {"name": "Grid Interface", "status": "AVAILABLE", "detail": "50 Hz nominal · simulated"},
            ],
            "trend": [
                round(total - 32 + 15 * math.sin((self._tick + i) / 3.5), 1)
                for i in range(24)
            ],
            "scope_notice": (
                "Presentation simulation for non-safety monitoring, balance-of-plant, "
                "historian, maintenance and training. Reactor protection, safety-class "
                "I&C, engineered safety actuation and SCRAM are outside this platform."
            ),
        }


executive_demo = ExecutiveDemo()
