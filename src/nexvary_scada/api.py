from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from nexvary_scada.drivers.base import DriverError, WriteBlockedError
from nexvary_scada.services.runtime import ScadaRuntime

PACKAGE_DIR = Path(__file__).resolve().parent
UI_DIR = PACKAGE_DIR / "ui"

app = FastAPI(title="NEXVARY SCADA", version="0.2.0")
runtime = ScadaRuntime()
app.mount("/static", StaticFiles(directory=UI_DIR), name="static")


class WriteRequest(BaseModel):
    value: bool | int | float | str


def identity(
    x_operator: str | None = Header(default=None),
    x_role: str | None = Header(default=None),
) -> tuple[str, str]:
    return (x_operator or "local-operator", (x_role or "viewer").lower())


@app.on_event("startup")
def startup_poll() -> None:
    if not runtime.last_values:
        runtime.poll()


@app.get("/")
def dashboard():
    return FileResponse(UI_DIR / "index.html")


@app.get("/api/status")
def status():
    active = runtime.alarms.events(active_only=True)
    return {
        "product": "NEXVARY SCADA",
        "version": "0.2.0",
        "mode": "INDUSTRIAL_RUNTIME",
        "active_alarms": len(active),
        "device_count": len(runtime.manager.devices()),
        "history_samples": runtime.historian.count(),
        "real_writes_default": "BLOCKED",
        "nuclear_scope": "NON_SAFETY_MONITORING_SIMULATION_ONLY",
    }


@app.get("/api/devices")
def devices():
    return runtime.manager.devices()


@app.get("/api/definitions")
def definitions():
    return [asdict(item) for item in runtime.manager.definitions()]


@app.get("/api/tags")
def tags():
    values = runtime.poll()
    definitions_by_id = {item.id: item for item in runtime.manager.definitions()}
    result = []
    for value in values:
        definition = definitions_by_id[value.tag_id]
        result.append({
            "tag_id": value.tag_id,
            "value": value.value,
            "quality": value.quality.value,
            "timestamp": value.timestamp.isoformat(),
            "device_id": value.device_id,
            "definition": asdict(definition),
        })
    return result


@app.get("/api/alarms")
def alarms(active_only: bool = False):
    result = []
    for event in runtime.alarms.events(active_only=active_only):
        item = asdict(event)
        item["severity"] = event.severity.value
        item["raised_at"] = event.raised_at.isoformat()
        item["changed_at"] = event.changed_at.isoformat()
        item["acknowledged_at"] = event.acknowledged_at.isoformat() if event.acknowledged_at else None
        result.append(item)
    return result


@app.post("/api/alarms/{rule_id}/ack")
def acknowledge_alarm(
    rule_id: str,
    x_operator: str | None = Header(default=None),
    x_role: str | None = Header(default=None),
):
    operator, role = x_operator or "local-operator", (x_role or "viewer").lower()
    try:
        event = runtime.acknowledge_alarm(rule_id, operator=operator, role=role)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown alarm") from exc
    except WriteBlockedError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return {"rule_id": event.rule_id, "acknowledged": event.acknowledged, "acknowledged_by": event.acknowledged_by}


@app.get("/api/history/{tag_id}")
def history(tag_id: str, limit: int = 50, minutes: int | None = None):
    if minutes is not None:
        return runtime.historian.window(tag_id, minutes=minutes, limit=limit)
    return runtime.historian.latest(tag_id, limit)


@app.get("/api/audit")
def audit(limit: int = 100):
    return runtime.audit.recent(limit)


@app.post("/api/write/{tag_id}")
def write_tag(
    tag_id: str,
    request: WriteRequest,
    x_operator: str | None = Header(default=None),
    x_role: str | None = Header(default=None),
):
    operator, role = x_operator or "local-operator", (x_role or "viewer").lower()
    try:
        value = runtime.write(tag_id, request.value, operator=operator, role=role)
    except WriteBlockedError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except DriverError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "tag_id": value.tag_id,
        "value": value.value,
        "quality": value.quality.value,
        "timestamp": value.timestamp.isoformat(),
        "device_id": value.device_id,
    }


@app.post("/api/simulator/{tag_id}")
def simulator_compat(
    tag_id: str,
    request: WriteRequest,
):
    return write_tag(tag_id, request, x_operator="local-operator", x_role="operator")


def main() -> None:
    uvicorn.run("nexvary_scada.api:app", host="127.0.0.1", port=8765, reload=False)


if __name__ == "__main__":
    main()
