from datetime import datetime, timedelta, timezone

from habit_tracker.analytics import current_streak, longest_streak_for_habit


def make_daily_checkoffs(days: int):
    now = datetime.now(timezone.utc)
    return [
        (now - timedelta(days=i)).isoformat()
        for i in range(days)
    ]


def make_weekly_checkoffs(weeks: int):
    now = datetime.now(timezone.utc)
    return [
        (now - timedelta(weeks=i)).isoformat()
        for i in range(weeks)
    ]


def test_daily_current_streak():
    checkoffs = make_daily_checkoffs(5)
    assert current_streak("daily", checkoffs) == 5


def test_daily_longest_streak():
    checkoffs = make_daily_checkoffs(10)
    assert longest_streak_for_habit("daily", checkoffs) == 10


def test_weekly_current_streak():
    checkoffs = make_weekly_checkoffs(4)
    assert current_streak("weekly", checkoffs) == 4


def test_weekly_longest_streak():
    checkoffs = make_weekly_checkoffs(6)
    assert longest_streak_for_habit("weekly", checkoffs) == 6


def test_daily_streak_with_gap():
    now = datetime.now(timezone.utc)
    checkoffs = [
        now.isoformat(),
        (now - timedelta(days=2)).isoformat(),  # gap
    ]
    assert current_streak("daily", checkoffs) == 1


def test_no_checkoffs():
    assert current_streak("daily", []) == 0