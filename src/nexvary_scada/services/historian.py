from __future__ import annotations

import json
import sqlite3
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
                value_json TEXT NOT NULL,
                quality TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )
        self.connection.execute("CREATE INDEX IF NOT EXISTS idx_history_tag_time ON tag_history(tag_id, timestamp)")
        self.connection.commit()

    def record(self, values: list[TagValue]) -> None:
        self.connection.executemany(
            "INSERT INTO tag_history(tag_id, value_json, quality, timestamp) VALUES (?, ?, ?, ?)",
            [(v.tag_id, json.dumps(v.value), v.quality.value, v.timestamp.isoformat()) for v in values],
        )
        self.connection.commit()

    def latest(self, tag_id: str, limit: int = 50) -> list[dict]:
        rows = self.connection.execute(
            "SELECT tag_id, value_json, quality, timestamp FROM tag_history WHERE tag_id=? ORDER BY id DESC LIMIT ?",
            (tag_id, limit),
        ).fetchall()
        return [
            {
                "tag_id": row["tag_id"],
                "value": json.loads(row["value_json"]),
                "quality": row["quality"],
                "timestamp": row["timestamp"],
            }
            for row in rows
        ]
