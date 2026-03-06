from datetime import datetime, timedelta, timezone
import sqlite3

from habit_tracker.db import connect, init_db
from habit_tracker.repository import HabitRepository

DB_PATH = "data/habits.sqlite"


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def ensure_habit(repo: HabitRepository, name: str, periodicity: str) -> int:
    """
    Create habit if it doesn't exist, return habit_id.
    Uses existing habit if already present.
    """
    # repository normalizes periodicity; name uniqueness is enforced by DB
    if repo.habit_name_exists(name):
        # find id
        row = repo.conn.execute(
            "SELECT id FROM habits WHERE name = ?",
            (name.strip(),),
        ).fetchone()
        return int(row["id"])

    habit = repo.create_habit(name, periodicity)
    return habit.id


def insert_checkoff(conn: sqlite3.Connection, habit_id: int, completed_at_iso: str) -> None:
    conn.execute(
        "INSERT INTO checkoffs (habit_id, completed_at) VALUES (?, ?)",
        (habit_id, completed_at_iso),
    )


def seed() -> None:
    conn = connect(DB_PATH)
    init_db(conn)
    repo = HabitRepository(conn)

    # ---- 5 predefined habits (at least one daily + one weekly) ----
    habits = [
        ("Drink Water", "daily"),
        ("Brush Teeth", "daily"),
        ("Read 10 Pages", "daily"),
        ("Gym Workout", "weekly"),
        ("Call Family", "weekly"),
    ]

    habit_ids = {}
    for name, period in habits:
        hid = ensure_habit(repo, name, period)
        habit_ids[name] = hid

    # ---- 4 weeks of example tracking data (last 28 days / last 4 ISO weeks) ----
    # Choose a fixed "end" point: today at 12:00 UTC (nice for consistent timestamps)
    end = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)

    # DAILY habits: add checkoffs over last 28 days with some intentional gaps
    # (helps demonstrate streak break behavior)
    daily_patterns = {
        "Drink Water":  {"skip_days": {6, 13, 20}},     # skips on these offsets
        "Brush Teeth":  {"skip_days": {}} ,             # perfect tracking
        "Read 10 Pages":{"skip_days": {2, 3, 17, 24}},  # some breaks
    }

    for habit_name, cfg in daily_patterns.items():
        hid = habit_ids[habit_name]
        skip = cfg["skip_days"]
        for offset in range(0, 28):  # 0..27 days back
            if offset in skip:
                continue
            dt = end - timedelta(days=offset)
            insert_checkoff(conn, hid, iso(dt))

    # WEEKLY habits: 4 checkoffs, one in each of the last 4 weeks
    # Use end - (0, 1, 2, 3) weeks, always at 12:00 UTC
    weekly_names = ["Gym Workout", "Call Family"]
    for habit_name in weekly_names:
        hid = habit_ids[habit_name]
        for w in range(0, 4):
            dt = end - timedelta(weeks=w)
            insert_checkoff(conn, hid, iso(dt))

    conn.commit()
    conn.close()

    print("✅ Seed complete:")
    print("   - 5 predefined habits created (or reused)")
    print("   - 4 weeks of checkoff data inserted")


if __name__ == "__main__":
    seed()
