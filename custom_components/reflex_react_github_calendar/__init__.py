"""reflex-react-github-calendar: a Reflex wrapper for react-github-calendar v5.

Public API::

    from reflex_react_github_calendar import github_calendar, GitHubCalendar
"""

from .github_calendar import (
    REACT_GITHUB_CALENDAR_VERSION,
    GitHubCalendar,
    github_calendar,
)

__version__ = "0.1.0"

__all__ = [
    "GitHubCalendar",
    "github_calendar",
    "REACT_GITHUB_CALENDAR_VERSION",
    "__version__",
]
