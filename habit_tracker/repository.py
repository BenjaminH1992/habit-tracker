from datetime import datetime, timezone
from typing import Optional

from .habit import Habit  #get Habit class


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class HabitRepository:
    def __init__(self, conn):
        self.conn = conn

    def habit_name_exists(self, name: str) -> bool:
        normalized = name.strip().lower()
        row = self.conn.execute(
            "SELECT 1 FROM habits WHERE lower(name) = ?",
            (normalized,)
        ).fetchone()
        return row is not None


    def create_habit(self, name: str, periodicity: str):
        # normalize before saving
        name = name.strip()
        periodicity = periodicity.strip().lower()

        created_at = datetime.now(timezone.utc).isoformat()

        cur = self.conn.execute(
            "INSERT INTO habits (name, periodicity, created_at) VALUES (?, ?, ?)",
            (name, periodicity, created_at)
        )
        self.conn.commit()

        return Habit(
            habit_id=int(cur.lastrowid),
            name=name,
            category=periodicity,
            created_at=created_at
        )
    

    def list_habits(self) -> list[Habit]:
        rows = self.conn.execute("SELECT * FROM habits ORDER BY id").fetchall()
        return [
            Habit(
                habit_id=int(r["id"]),
                name=str(r["name"]),
                category=str(r["periodicity"]),
                created_at=str(r["created_at"]),
            )
            for r in rows
        ]

    def get_habit_by_id(self, habit_id: int) -> Optional[Habit]:
        r = self.conn.execute("SELECT * FROM habits WHERE id = ?", (habit_id,)).fetchone()
        if not r:
            return None
        return Habit(
            habit_id=int(r["id"]),
            name=str(r["name"]),
            category=str(r["periodicity"]),
            created_at=str(r["created_at"]),
        )

    def delete_habit(self, habit_id: int) -> bool:
        cur = self.conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def add_checkoff(self, habit_id: int) -> None:
        self.conn.execute(
            "INSERT INTO checkoffs(habit_id, completed_at) VALUES (?, ?)",
            (habit_id, now_iso()),
        )
        self.conn.commit()

    def list_checkoffs(self, habit_id: int) -> list[str]:
        rows = self.conn.execute(
            "SELECT completed_at FROM checkoffs WHERE habit_id = ? ORDER BY completed_at",
            (habit_id,),
        ).fetchall()
        return [str(r["completed_at"]) for r in rows]