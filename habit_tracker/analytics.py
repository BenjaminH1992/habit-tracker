from __future__ import annotations

from datetime import datetime, timezone, date
from typing import Iterable
from datetime import timedelta
from typing import List, Tuple, Union, Set 


def _parse_iso(ts: str) -> datetime:
    # Timestamp
    return datetime.fromisoformat(ts)


def _daily_keys(checkoffs: Iterable[str]) -> list[date]:
    # unique days
    return sorted({_parse_iso(ts).date() for ts in checkoffs})


def _weekly_keys(checkoffs: Iterable[str]) -> list[tuple[int, int]]:
    # unique weeks
    keys = set()
    for ts in checkoffs:
        iso = _parse_iso(ts).isocalendar()
        keys.add((iso[0], iso[1]))  # year, week
    return sorted(keys)


def current_streak(periodicity: str, checkoffs: list[str]) -> int:
    """
    Returns the current streak.
    Daily: consecutive days including today.
    Weekly: consecutive ISO weeks including current week.
    """
    periodicity = periodicity.lower().strip()
    if not checkoffs:
        return 0

    now = datetime.now(timezone.utc)

    if periodicity == "daily":
        days = set(_daily_keys(checkoffs))
        today = now.date()

        if today not in days:
            return 0

        streak = 0
        d = today
        while d in days:
            streak += 1
            d = date.fromordinal(d.toordinal() - 1)  # previous day
        return streak

    if periodicity == "weekly":
        weeks = set(_weekly_keys(checkoffs))
        iso = now.isocalendar()
        cur = (iso[0], iso[1])

        if cur not in weeks:
            return 0

        # Represent (year, week) as a monotonically increasing number
        # using y*53 + w (53 is max ISO weeks)
        def num(yw: tuple[int, int]) -> int:
            y, w = yw
            return y * 53 + w

        streak = 0
        n = num(cur)
        while True:
            y = n // 53
            w = n % 53
            if w == 0:
                # adjust, because week numbers start at 1
                y -= 1
                w = 53
            if (y, w) in weeks:
                streak += 1
                n -= 1
            else:
                break
        return streak

    raise ValueError("periodicity must be 'daily' or 'weekly'")

WeekKey = Tuple[int, int]  # (iso_year, iso_week)
Key = Union[date, WeekKey]

#longest streak archived so far
def _longest_consecutive_run(keys: List[Key]) -> int:
    """
    keys must be sorted and unique.
    Supports date keys (daily) and (year, week) keys (weekly).
    """
    if not keys:
        return 0

    # Daily case: consecutive dates differ by 1 day
    if isinstance(keys[0], date):
        best = 1
        cur = 1
        for prev, nxt in zip(keys, keys[1:]):
            if (nxt - prev).days == 1:
                cur += 1
            else:
                best = max(best, cur)
                cur = 1
        return max(best, cur)

    # Weekly case: treat (year, week) as monotonic numbers
    # using year*53 + week (53 is max ISO weeks)
    def num(yw: WeekKey) -> int:
        return yw[0] * 53 + yw[1]

    nums = [num(k) for k in keys]  # type: ignore[arg-type]
    best = 1
    cur = 1
    for prev, nxt in zip(nums, nums[1:]):
        if nxt - prev == 1:
            cur += 1
        else:
            best = max(best, cur)
            cur = 1
    return max(best, cur)

#longest overall streak for all habits
def longest_streak_for_habit(periodicity: str, checkoffs: List[str]) -> int:
    """
    Longest streak across all history for a single habit.
    - daily: longest run of consecutive days with >=1 checkoff
    - weekly: longest run of consecutive ISO weeks with >=1 checkoff
    """
    periodicity = periodicity.strip().lower()
    if not checkoffs:
        return 0

    if periodicity == "daily":
        # unique day keys sorted
        keys = sorted({_parse_iso(ts).date() for ts in checkoffs})
        return _longest_consecutive_run(keys)

    if periodicity == "weekly":
        # unique ISO week keys sorted
        week_keys: Set[WeekKey] = set()
        for ts in checkoffs:
            iso = _parse_iso(ts).isocalendar()
            # Python 3.7-safe tuple indexing:
            week_keys.add((iso[0], iso[1]))
        keys2 = sorted(week_keys)
        return _longest_consecutive_run(keys2)

    raise ValueError("periodicity must be 'daily' or 'weekly'")

def total_sparkles_from_habits(habits, get_checkoffs_for_habit) -> int:
    """
    Returns total sparkles across all habits.
    Sparkles are earned based on longest streak achieved for each habit:
    - daily: 1 sparkle per 7 streak
    - weekly: 1 sparkle per 4 streak
    """
    total = 0

    for h in habits:
        checkoffs = get_checkoffs_for_habit(h.id)
        longest = longest_streak_for_habit(h.category, checkoffs)

        if h.category == "daily":
            total += longest // 7
        elif h.category == "weekly":
            total += longest // 4

    return total


def convert_sparkles(sparkles: int):
    """
    Converts sparkles into stars and superstars.
    5 ✨ -> 1 ⭐
    5 ⭐ -> 1 🌟
    Returns (superstars, stars, remaining_sparkles)
    """
    stars, remaining_sparkles = divmod(sparkles, 5)
    superstars, remaining_stars = divmod(stars, 5)
    return superstars, remaining_stars, remaining_sparkles