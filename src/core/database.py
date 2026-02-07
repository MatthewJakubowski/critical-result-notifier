import sqlite3
import logging
from dataclasses import dataclass

@dataclass
class Incident:
    id: int
    order_id: str
    phone: str
    status: str
    retries: int

class IncidentDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id TEXT UNIQUE,
                    value REAL,
                    phone TEXT,
                    status TEXT DEFAULT 'NEW',
                    retries INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def create_incident(self, order_id, value, phone):
        try:
            with self._get_conn() as conn:
                conn.execute(
                    "INSERT OR IGNORE INTO incidents (order_id, value, phone, status) VALUES (?, ?, ?, 'NEW')",
                    (order_id, value, phone)
                )
                return True
        except Exception as e:
            logging.error(f"DB Error: {e}")
            return False

    def get_pending(self):
        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM incidents WHERE status IN ('NEW', 'PROCESSING', 'ESCALATING')").fetchall()
            return [Incident(r['id'], r['order_id'], r['phone'], r['status'], r['retries']) for r in rows]

    def update_status(self, incident_id, status, increment_retry=False):
        with self._get_conn() as conn:
            retry_sql = ", retries = retries + 1" if increment_retry else ""
            conn.execute(f"UPDATE incidents SET status = ?, updated_at = CURRENT_TIMESTAMP {retry_sql} WHERE id = ?", (status, incident_id))
