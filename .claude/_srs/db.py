"""SQLite DAL for state.db.

Single physical table `studylog` (append-only, post-review snapshots) plus a
view `vw_cards` exposing the latest row per card_id. No `cards` table — card
state is the most recent studylog row for that card_id, and card_path is
derived from the filesystem walk (not stored).
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

_SCHEMA = """
CREATE TABLE IF NOT EXISTS studylog (
    study_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id       TEXT NOT NULL,
    timestamp     TEXT NOT NULL,
    state_vector  TEXT NOT NULL,
    state_type    TEXT NOT NULL,
    grade         INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_studylog_card_time
    ON studylog(card_id, timestamp DESC);

CREATE VIEW IF NOT EXISTS vw_cards AS
SELECT
    s.card_id,
    s.state_vector,
    s.state_type,
    s.timestamp AS last_updated
FROM studylog s
JOIN (
    SELECT card_id, MAX(study_id) AS max_id
    FROM studylog
    GROUP BY card_id
) latest
  ON latest.card_id = s.card_id AND latest.max_id = s.study_id;
"""


def connect(db_path: Path) -> sqlite3.Connection:
    """Open (or create) state.db and ensure the schema exists."""
    conn = sqlite3.connect(db_path)
    conn.executescript(_SCHEMA)
    conn.commit()
    return conn


def latest_state(conn: sqlite3.Connection, card_id: str) -> tuple[str, str, datetime] | None:
    """Return (state_vector_json, state_type, last_updated) or None if never reviewed."""
    row = conn.execute(
        "SELECT state_vector, state_type, last_updated FROM vw_cards WHERE card_id = ?",
        (card_id,),
    ).fetchone()
    if row is None:
        return None
    sv, st, ts = row
    return sv, st, _parse_ts(ts)


def list_latest_states(conn: sqlite3.Connection) -> dict[str, tuple[str, str, datetime]]:
    """Map every reviewed card_id → (state_vector, state_type, last_updated)."""
    out: dict[str, tuple[str, str, datetime]] = {}
    for cid, sv, st, ts in conn.execute(
        "SELECT card_id, state_vector, state_type, last_updated FROM vw_cards"
    ):
        out[cid] = (sv, st, _parse_ts(ts))
    return out


def insert_review(
    conn: sqlite3.Connection,
    *,
    card_id: str,
    timestamp: datetime,
    state_vector_json: str,
    state_type: str,
    grade: int,
) -> None:
    conn.execute(
        "INSERT INTO studylog (card_id, timestamp, state_vector, state_type, grade) "
        "VALUES (?, ?, ?, ?, ?)",
        (card_id, timestamp.isoformat(), state_vector_json, state_type, grade),
    )
    conn.commit()


def _parse_ts(ts: str) -> datetime:
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt
