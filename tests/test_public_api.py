"""The Phase 3 helpers and domain types are re-exported at the top level."""

from __future__ import annotations

import reflex_react_github_calendar as pkg


def test_top_level_exports() -> None:
    for name in (
        "GitHubCalendar",
        "github_calendar",
        "REACT_GITHUB_CALENDAR_VERSION",
        "Theme",
        "last_n_days",
        "last_half_year",
        "activity_tooltip",
        "link_blocks",
    ):
        assert name in pkg.__all__, f"{name} missing from __all__"
        assert hasattr(pkg, name), f"{name} not importable from package"