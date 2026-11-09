"""Shared utility functions for templates and routes."""

from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database import Todo


def _as_date(dt: datetime | date) -> date:
    """Due dates are calendar days, so compare without the time of day."""
    return dt.date() if isinstance(dt, datetime) else dt


def is_overdue(todo: "Todo") -> bool:
    """Return True if due_date < today AND not completed."""
    if todo.is_completed or not todo.due_date:
        return False
    return _as_date(todo.due_date) < date.today()


def is_due_today(todo: "Todo") -> bool:
    """Return True if due_date == today."""
    if not todo.due_date:
        return False
    return _as_date(todo.due_date) == date.today()


def format_date(dt: datetime | date | None) -> str:
    """Format a date for display."""
    if dt is None:
        return ""
    if isinstance(dt, datetime):
        dt = dt.date()
    return dt.strftime("%b %d, %Y")


def format_date_input(dt: datetime | date | None) -> str:
    """Format a date for HTML date input (YYYY-MM-DD)."""
    if dt is None:
        return ""
    if isinstance(dt, datetime):
        dt = dt.date()
    return dt.strftime("%Y-%m-%d")
