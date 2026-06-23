"""Contract tests: the rendered React surface must match the spec.

These lock in the snake_case -> camelCase prop mapping (ADR-4) and the v5
import wiring (ADR-1/ADR-2) at the render level, so the behavior that the
Phase 1/2 manual tasks verify in a browser is also guarded automatically.

`Component.render()` returns ``{"name", "props", "children"}`` where each prop
is a ``"camelCaseName:value"`` string.
"""

from __future__ import annotations

import reflex as rx

from reflex_react_github_calendar import github_calendar


def _prop_names(component: rx.Component) -> set[str]:
    """The camelCase prop names emitted in the rendered output."""
    return {entry.split(":", 1)[0] for entry in component.render()["props"]}


def test_renders_named_tag() -> None:
    """The emitted React tag is the v5 named export ``GitHubCalendar``."""
    assert github_calendar(username="grubersjoe").render()["name"] == "GitHubCalendar"


def test_snake_case_props_become_camel_case() -> None:
    """Every snake_case prop maps to its documented camelCase React name."""
    component = github_calendar(
        username="grubersjoe",
        block_size=12,
        block_margin=4,
        block_radius=2,
        font_size=14,
        color_scheme="dark",
        max_level=4,
        min_level=0,
        show_color_legend=False,
        show_month_labels=True,
        show_total_count=True,
        show_weekday_labels=True,
        week_start=1,
        throw_on_error=True,
        error_message="boom",
    )
    names = _prop_names(component)
    expected = {
        "blockSize",
        "blockMargin",
        "blockRadius",
        "fontSize",
        "colorScheme",
        "maxLevel",
        "minLevel",
        "showColorLegend",
        "showMonthLabels",
        "showTotalCount",
        "showWeekdayLabels",
        "weekStart",
        "throwOnError",
        "errorMessage",
        "username",
    }
    assert expected.issubset(names)


def test_year_accepts_literal_last_and_integer() -> None:
    """``year`` carries through as both the literal "last" and an int (FR-2)."""
    last_props = github_calendar(username="grubersjoe", year="last").render()["props"]
    int_props = github_calendar(username="grubersjoe", year=2024).render()["props"]
    assert any(p.startswith("year:") and "last" in p for p in last_props)
    assert any(p.startswith("year:") and "2024" in p for p in int_props)
