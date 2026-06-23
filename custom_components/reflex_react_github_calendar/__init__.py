"""reflex-react-github-calendar: a Reflex wrapper for react-github-calendar v5.

Public API::

    from reflex_react_github_calendar import github_calendar, GitHubCalendar

    # DDD value object for custom themes:
    from reflex_react_github_calendar import Theme

    # Phase 3 helpers for the advanced, function-valued props:
    from reflex_react_github_calendar import (
        last_n_days, last_half_year, activity_tooltip, link_blocks,
    )
"""

from .domain import Theme
from .github_calendar import (
    REACT_GITHUB_CALENDAR_VERSION,
    GitHubCalendar,
    github_calendar,
)
from .recipes import (
    activity_tooltip,
    last_half_year,
    last_n_days,
    link_blocks,
)

__version__ = "0.1.0"

__all__ = [
    "GitHubCalendar",
    "github_calendar",
    "REACT_GITHUB_CALENDAR_VERSION",
    "Theme",
    "last_n_days",
    "last_half_year",
    "activity_tooltip",
    "link_blocks",
    "__version__",
]
