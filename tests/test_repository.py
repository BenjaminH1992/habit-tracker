from habit_tracker.repository import HabitRepository
from habit_tracker.db import init_db
from habit_tracker.main import ensure_predefined_habits
import sqlite3

def make_test_repo():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    return HabitRepository(conn)


def test_create_habit():
    repo = make_test_repo()
    habit = repo.create_habit("Test Habit", "daily")

    assert habit.name == "Test Habit"
    assert habit.category == "daily"


def test_add_checkoff():
    repo = make_test_repo()
    habit = repo.create_habit("Drink Water", "daily")

    repo.add_checkoff(habit.id)
    checkoffs = repo.list_checkoffs(habit.id)

    assert len(checkoffs) == 1

def make_test_repo():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    return HabitRepository(conn)


def test_ensure_predefined_habits_creates_five_habits():
    repo = make_test_repo()

    ensure_predefined_habits(repo)
    habits = repo.list_habits()

    assert len(habits) == 5

def test_ensure_predefined_habits_does_not_duplicate():
    repo = make_test_repo()

    ensure_predefined_habits(repo)
    ensure_predefined_habits(repo)

    habits = repo.list_habits()

    assert len(habits) == 5