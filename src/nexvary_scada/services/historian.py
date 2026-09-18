from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

from nexvary_scada.models import TagValue


class Historian:
    def __init__(self, database: str | Path = ":memory:") -> None:
        self.connection = sqlite3.connect(str(database), check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tag_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag_id TEXT NOT NULL,
                device_id TEXT NOT NULL DEFAULT '',
                value_json TEXT NOT NULL,
                quality TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )
        columns = {row["name"] for row in self.connection.execute("PRAGMA table_info(tag_history)").fetchall()}
        if "device_id" not in columns:
            self.connection.execute("ALTER TABLE tag_history ADD COLUMN device_id TEXT NOT NULL DEFAULT ''")
        self.connection.execute("CREATE INDEX IF NOT EXISTS idx_history_tag_time ON tag_history(tag_id, timestamp)")
        self.connection.commit()

    def record(self, values: list[TagValue]) -> None:
        self.connection.executemany(
            "INSERT INTO tag_history(tag_id, device_id, value_json, quality, timestamp) VALUES (?, ?, ?, ?, ?)",
            [(v.tag_id, v.device_id, json.dumps(v.value), v.quality.value, v.timestamp.isoformat()) for v in values],
        )
        self.connection.commit()

    @staticmethod
    def _row(row: sqlite3.Row) -> dict:
        return {
            "tag_id": row["tag_id"],
            "device_id": row["device_id"],
            "value": json.loads(row["value_json"]),
            "quality": row["quality"],
            "timestamp": row["timestamp"],
        }

    def latest(self, tag_id: str, limit: int = 50) -> list[dict]:
        rows = self.connection.execute(
            "SELECT tag_id, device_id, value_json, quality, timestamp FROM tag_history WHERE tag_id=? ORDER BY id DESC LIMIT ?",
            (tag_id, min(max(int(limit), 1), 5000)),
        ).fetchall()
        return [self._row(row) for row in rows]

    def window(self, tag_id: str, *, minutes: int = 60, limit: int = 1000) -> list[dict]:
        since = (datetime.now(UTC) - timedelta(minutes=max(1, minutes))).isoformat()
        rows = self.connection.execute(
            """
            SELECT tag_id, device_id, value_json, quality, timestamp
            FROM tag_history
            WHERE tag_id=? AND timestamp>=?
            ORDER BY id ASC
            LIMIT ?
            """,
            (tag_id, since, min(max(int(limit), 1), 5000)),
        ).fetchall()
        return [self._row(row) for row in rows]

    def count(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM tag_history").fetchone()[0])
