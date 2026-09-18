from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuditLog:
    def __init__(self, database: str | Path = ":memory:") -> None:
        self.connection = sqlite3.connect(str(database), check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                operator TEXT NOT NULL,
                role TEXT NOT NULL,
                action TEXT NOT NULL,
                target TEXT NOT NULL,
                success INTEGER NOT NULL,
                detail_json TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def record(
        self,
        *,
        operator: str,
        role: str,
        action: str,
        target: str,
        success: bool,
        detail: dict[str, Any] | None = None,
    ) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        self.connection.execute(
            "INSERT INTO audit_log(timestamp, operator, role, action, target, success, detail_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (timestamp, operator, role, action, target, int(success), json.dumps(detail or {}, ensure_ascii=False)),
        )
        self.connection.commit()

    def recent(self, limit: int = 100) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT * FROM audit_log ORDER BY id DESC LIMIT ?",
            (min(max(int(limit), 1), 1000),),
        ).fetchall()
        return [
            {
                "id": row["id"],
                "timestamp": row["timestamp"],
                "operator": row["operator"],
                "role": row["role"],
                "action": row["action"],
                "target": row["target"],
                "success": bool(row["success"]),
                "detail": json.loads(row["detail_json"]),
            }
            for row in rows
        ]
