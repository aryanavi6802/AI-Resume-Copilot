"""SQLite database for analysis history persistence."""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "analysis_history.db"
)


def _get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the analysis_history table if it does not exist."""
    conn = _get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            resume_filename TEXT NOT NULL,
            job_title TEXT DEFAULT '',
            match_score INTEGER DEFAULT 0,
            status TEXT DEFAULT '',
            sponsorship_flag INTEGER DEFAULT 0,
            analysis_json TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def save_analysis(
    resume_filename: str,
    job_title: str,
    match_score: int,
    status: str,
    sponsorship_flag: bool,
    analysis_json: str,
) -> int:
    """Insert a new analysis record and return its id."""
    conn = _get_connection()
    cursor = conn.execute(
        """INSERT INTO analysis_history
        (timestamp, resume_filename, job_title, match_score, status,
         sponsorship_flag, analysis_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            datetime.now().isoformat(),
            resume_filename,
            job_title,
            match_score,
            status,
            int(sponsorship_flag),
            analysis_json,
        ),
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def get_all_analyses() -> List[dict]:
    """Return all analyses ordered by most recent first."""
    conn = _get_connection()
    rows = conn.execute(
        "SELECT * FROM analysis_history ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_analysis_by_id(analysis_id: int) -> Optional[dict]:
    """Return a single analysis record by id."""
    conn = _get_connection()
    row = conn.execute(
        "SELECT * FROM analysis_history WHERE id = ?", (analysis_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def search_analyses(query: str) -> List[dict]:
    """Search analyses by filename, job title, or status."""
    conn = _get_connection()
    rows = conn.execute(
        """SELECT * FROM analysis_history
        WHERE resume_filename LIKE ? OR job_title LIKE ? OR status LIKE ?
        ORDER BY timestamp DESC""",
        (f"%{query}%", f"%{query}%", f"%{query}%"),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
