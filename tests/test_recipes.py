"""Tests for the Phase 3 advanced function-prop helpers (``recipes.py``).

The advanced props (``transform_data``, ``render_block``, ``tooltips``) take
JavaScript functions and must be passed as raw ``Var``s (ADR-6). These helpers
build those ``Var``s from a plain-Python API so consumers never hand-write JS.
The function body runs in the browser; here we assert the generated JS surface.
"""

from __future__ import annotations

import json

import pytest
import reflex as rx

from reflex_react_github_calendar.recipes import (
    activity_tooltip,
    last_half_year,
    last_n_days,
    link_blocks,
)


def test_last_n_days_returns_var() -> None:
    var = last_n_days(90)
    assert isinstance(var, rx.Var)
    js = str(var)
    assert js.startswith("(data) =>")
    assert "slice(-90)" in js


def test_last_n_days_rejects_non_positive() -> None:
    with pytest.raises(ValueError, match="positive"):
        last_n_days(0)


def test_last_half_year_filters_by_date() -> None:
    js = str(last_half_year())
    assert "filter" in js
    assert "setMonth" in js


def test_activity_tooltip_builds_tooltip_object() -> None:
    js = str(activity_tooltip("{{count}} contributions on {{date}}"))
    assert "activity" in js
    assert "text" in js
    # The template is embedded JSON-encoded so quotes/specials stay safe.
    assert json.dumps("{{count}} contributions on {{date}}") in js


def test_activity_tooltip_substitutes_placeholders() -> None:
    js = str(activity_tooltip("{{count}} on {{date}}"))
    assert "{{count}}" in js  # placeholder referenced for replacement
    assert "{{date}}" in js
    assert "activity.count" in js
    assert "activity.date" in js


def test_link_blocks_wraps_block_in_anchor() -> None:
    js = str(link_blocks("https://github.com/grubersjoe"))
    assert "(block, activity) =>" in js
    assert "createElement" in js
    assert json.dumps("https://github.com/grubersjoe") in js


def test_helpers_render_as_props() -> None:
    """Helpers can be passed straight to the component props."""
    from reflex_react_github_calendar import github_calendar

    comp = github_calendar(
        username="grubersjoe",
        transform_data=last_n_days(30),
        tooltips=activity_tooltip("{{count}} on {{date}}"),
        render_block=link_blocks("https://github.com/{{date}}"),
    )
    props = comp.render()["props"]
    assert any(p.startswith("transformData:") for p in props)
    assert any(p.startswith("tooltips:") for p in props)
    assert any(p.startswith("renderBlock:") for p in props)
