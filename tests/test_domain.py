"""Tests for the DDD domain value objects (``domain.py``).

``Theme`` is a value object modelling a custom calendar color theme. It
validates the upstream invariant — each color scale must be a ``[zero, max]``
pair (interpolated) or exactly ``max_level + 1`` explicit colors — and produces
the plain dict the ``theme`` prop expects.
"""

from __future__ import annotations

import pytest

from reflex_react_github_calendar.domain import Theme


def test_two_color_scale_to_prop() -> None:
    theme = Theme(light=["#eee", "firebrick"])
    assert theme.to_prop() == {"light": ["#eee", "firebrick"]}


def test_explicit_five_color_scale_to_prop() -> None:
    colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    theme = Theme(light=colors, dark=colors)
    assert theme.to_prop() == {"light": colors, "dark": colors}


def test_dark_is_optional() -> None:
    assert "dark" not in Theme(light=["#eee", "#222"]).to_prop()


def test_invalid_scale_length_raises() -> None:
    with pytest.raises(ValueError, match="2 or 5 colors"):
        Theme(light=["#eee", "#777", "#222"])  # 3 colors is invalid


def test_empty_scale_raises() -> None:
    with pytest.raises(ValueError, match="2 or 5 colors"):
        Theme(light=[])


def test_theme_is_immutable() -> None:
    theme = Theme(light=["#eee", "#222"])
    with pytest.raises(Exception):
        theme.light = ["#000", "#fff"]  # type: ignore[misc]
