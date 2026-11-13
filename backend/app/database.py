"""
Aushadha Sathi - Database Connectivity Layer
Provides database verification for system health monitoring while enforcing zero patient persistence.
Compliance: DPDP Act 2023 §8(7) (Zero Disk Persistence for clinical and prescription data).
"""

import os
import sqlite3
from typing import Optional, Tuple

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "health.db")
DATABASE_URL = os.getenv("DATABASE_URL", "")


def get_db_connection() -> sqlite3.Connection:
    """Returns a SQLite connection for health monitoring."""
    if DATABASE_URL.startswith("sqlite:///"):
        path = DATABASE_URL.replace("sqlite:///", "")
    elif DATABASE_URL == ":memory:":
        path = ":memory:"
    else:
        path = DEFAULT_DB_PATH

    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: Optional[sqlite3.Connection] = None) -> None:
    """Initializes the health monitoring table and seeds initial record."""
    should_close = False
    if conn is None:
        conn = get_db_connection()
        should_close = True

    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS system_health (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    check_key TEXT UNIQUE NOT NULL,
                    status_value TEXT NOT NULL,
                    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.execute(
                """
                INSERT OR IGNORE INTO system_health (check_key, status_value)
                VALUES ('health_check', 'Database connection healthy (SQLite)');
                """
            )
    finally:
        if should_close:
            conn.close()


def read_health_value() -> Tuple[str, str]:
    """
    Reads a health record directly from the database table.
    Returns:
        (status, value) e.g. ("connected", "Database connection healthy (SQLite)")
    """
    try:
        conn = get_db_connection()
        try:
            init_db(conn)
            cur = conn.cursor()
            cur.execute(
                "SELECT status_value FROM system_health WHERE check_key = 'health_check' LIMIT 1;"
            )
            row = cur.fetchone()
            if row and row["status_value"]:
                return "connected", str(row["status_value"])
            return "connected", "Database operational (no seed record)"
        finally:
            conn.close()
    except Exception as exc:
        return "disconnected", f"Database query failed: {exc}"
