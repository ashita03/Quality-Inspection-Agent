import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).parent.parent / "qc_agent.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_id TEXT,
            image_path TEXT,
            defect_detected INTEGER,
            defect_type TEXT,
            confidence REAL,
            verdict TEXT,
            reasoning_trace TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_inspection(state: dict):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO inspections
            (part_id, image_path, defect_detected, defect_type, confidence, verdict, reasoning_trace, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            state.get("part_id"),
            state.get("image_path"),
            int(bool(state.get("defect_detected"))),
            state.get("defect_type"),
            state.get("confidence"),
            state.get("verdict"),
            " | ".join(state.get("reasoning_trace", [])),
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def count_recent_defects(defect_type: str, limit_rows: int = 20) -> int:
    if not defect_type or defect_type == "none":
        return 0
    conn = get_connection()
    rows = conn.execute(
        "SELECT defect_type FROM inspections ORDER BY id DESC LIMIT ?",
        (limit_rows,),
    ).fetchall()
    conn.close()
    return sum(1 for r in rows if r["defect_type"] == defect_type)


if __name__ == "__main__":
    init_db()
    print(f"Initialized DB at {DB_PATH}")