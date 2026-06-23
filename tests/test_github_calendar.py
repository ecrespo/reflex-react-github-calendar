"""Smoke tests for the reflex-react-github-calendar wrapper.

These verify the React wiring that is easy to get wrong when wrapping a
third-party component (library/tag/export style) and that props are exposed.
They do not require a running browser.
"""

from __future__ import annotations

import reflex as rx

from reflex_react_github_calendar import (
    REACT_GITHUB_CALENDAR_VERSION,
    GitHubCalendar,
    github_calendar,
)


def test_library_wiring() -> None:
    """The component must import the v5 named export from the pinned package."""
    assert REACT_GITHUB_CALENDAR_VERSION.startswith("react-github-calendar@")
    assert GitHubCalendar.library == REACT_GITHUB_CALENDAR_VERSION
    assert GitHubCalendar.tag == "GitHubCalendar"
    # v5 dropped the default export — must be a named import.
    assert GitHubCalendar.is_default is False


def test_is_no_ssr_component() -> None:
    """The calendar fetches data client-side, so SSR must be disabled."""
    from reflex.components.component import NoSSRComponent

    assert issubclass(GitHubCalendar, NoSSRComponent)


def test_create_returns_component() -> None:
    comp = github_calendar(username="grubersjoe")
    assert isinstance(comp, GitHubCalendar)


def test_core_props_declared() -> None:
    """A representative set of props must be present on the class."""
    expected = {
        "username",
        "year",
        "block_size",
        "color_scheme",
        "theme",
        "show_color_legend",
        "show_month_labels",
        "show_weekday_labels",
        "labels",
    }
    assert expected.issubset(set(GitHubCalendar.get_fields()))
