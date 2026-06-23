"""Tests for the opt-in tooltip stylesheet injection (ADR-7).

v5 tooltips are headless. Consumers may opt into the bundled stylesheet by
passing ``include_tooltip_styles=True``; the component then emits an
``import "react-github-calendar/styles.css";`` line via ``_get_custom_code``.
Styles are never forced (ADR-7), and the flag must not leak into rendered props.
"""

from __future__ import annotations

from reflex_react_github_calendar import github_calendar


def test_no_styles_by_default() -> None:
    assert github_calendar(username="grubersjoe")._get_custom_code() is None


def test_opt_in_imports_stylesheet() -> None:
    code = github_calendar(
        username="grubersjoe", include_tooltip_styles=True
    )._get_custom_code()
    assert code is not None
    assert "react-github-calendar/styles.css" in code


def test_flag_does_not_leak_into_props() -> None:
    comp = github_calendar(username="grubersjoe", include_tooltip_styles=True)
    rendered = comp.render()
    joined = " ".join(rendered["props"])
    assert "includeTooltipStyles" not in joined
    assert "include_tooltip_styles" not in joined