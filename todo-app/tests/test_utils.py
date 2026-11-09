"""Tests for the due-date helpers that drive overdue and due-today styling."""

from datetime import datetime, timedelta
from types import SimpleNamespace

from app.utils import is_due_today, is_overdue


def _todo(due_date, is_completed=False):
    return SimpleNamespace(due_date=due_date, is_completed=is_completed)


def _midnight(days_from_today):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return today + timedelta(days=days_from_today)


class TestDueDates:
    """A due date is a calendar day: the time of day must not matter."""

    def test_yesterday_is_overdue(self):
        assert is_overdue(_todo(_midnight(-1))) is True

    def test_today_is_due_today_not_overdue(self):
        todo = _todo(_midnight(0))
        assert is_overdue(todo) is False
        assert is_due_today(todo) is True

    def test_tomorrow_is_neither(self):
        todo = _todo(_midnight(1))
        assert is_overdue(todo) is False
        assert is_due_today(todo) is False

    def test_completed_todo_is_never_overdue(self):
        assert is_overdue(_todo(_midnight(-1), is_completed=True)) is False
