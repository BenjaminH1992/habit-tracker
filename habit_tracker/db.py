import sqlite3

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    periodicity TEXT NOT NULL CHECK(periodicity IN ('daily', 'weekly')),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS checkoffs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    completed_at TEXT NOT NULL,
    FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_checkoffs_habit_id ON checkoffs(habit_id);
CREATE INDEX IF NOT EXISTS idx_checkoffs_completed_at ON checkoffs(completed_at);
"""

def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()

print("db.py loaded")