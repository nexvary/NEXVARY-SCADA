from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from nexvary_scada.drivers.base import DriverError
from nexvary_scada.services.runtime import ScadaRuntime

PACKAGE_DIR = Path(__file__).resolve().parent
UI_DIR = PACKAGE_DIR / "ui"

app = FastAPI(title="NEXVARY SCADA", version="0.1.0")
runtime = ScadaRuntime()
app.mount("/static", StaticFiles(directory=UI_DIR), name="static")


class WriteRequest(BaseModel):
    value: bool | int | float | str


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
        "version": "0.1.0",
        "driver": runtime.driver.name,
        "mode": "SIMULATION",
        "active_alarms": len(active),
        "write_policy": "SIMULATOR_ONLY",
        "nuclear_scope": "NON_SAFETY_MONITORING_SIMULATION_ONLY",
    }


@app.get("/api/tags")
def tags():
    values = runtime.poll()
    definitions = {item.id: item for item in runtime.driver.definitions()}
    return [
        {
            **asdict(value),
            "timestamp": value.timestamp.isoformat(),
            "quality": value.quality.value,
            "definition": asdict(definitions[value.tag_id]),
        }
        for value in values
    ]


@app.get("/api/alarms")
def alarms(active_only: bool = False):
    return [
        {
            **asdict(event),
            "severity": event.severity.value,
            "raised_at": event.raised_at.isoformat(),
            "changed_at": event.changed_at.isoformat(),
        }
        for event in runtime.alarms.events(active_only=active_only)
    ]


@app.get("/api/history/{tag_id}")
def history(tag_id: str, limit: int = 50):
    return runtime.historian.latest(tag_id, min(max(limit, 1), 500))


@app.post("/api/simulator/{tag_id}")
def simulator_write(tag_id: str, request: WriteRequest):
    try:
        value = runtime.write_simulated(tag_id, request.value)
    except DriverError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "tag_id": value.tag_id,
        "value": value.value,
        "quality": value.quality.value,
        "timestamp": value.timestamp.isoformat(),
    }


def main() -> None:
    uvicorn.run("nexvary_scada.api:app", host="127.0.0.1", port=8765, reload=False)


if __name__ == "__main__":
    main()
