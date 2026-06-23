"""Ergonomic helpers for the advanced, function-valued props (Phase 3).

``transform_data``, ``render_block`` and ``tooltips`` accept JavaScript
functions on the React side, so they must be passed as raw function ``Var``s
(ADR-6). These recipes build those ``Var``s from a plain-Python API — the common
cases from the upstream demo — so consumers never hand-write JavaScript.

Each helper returns an ``rx.Var`` carrying a JS expression; pass it straight to
the matching prop::

    from reflex_react_github_calendar import github_calendar
    from reflex_react_github_calendar.recipes import last_n_days

    github_calendar(username="grubersjoe", transform_data=last_n_days(90))
"""

from __future__ import annotations

import json

import reflex as rx


def last_n_days(n: int) -> rx.Var:
    """``transform_data`` recipe: keep only the last ``n`` day entries.

    Mirrors the upstream ``(data) => data.slice(-90)`` example.
    """
    if n <= 0:
        raise ValueError(f"n must be a positive number of days, got {n}")
    return rx.Var(f"(data) => data.slice(-{n})")


def last_half_year() -> rx.Var:
    """``transform_data`` recipe: keep entries from the last six months.

    Reproduces the demo's "last half year" example by filtering activities
    whose ``date`` is on or after a cutoff six months before today.
    """
    return rx.Var(
        "(data) => {"
        " const cutoff = new Date();"
        " cutoff.setMonth(cutoff.getMonth() - 6);"
        " return data.filter((activity) => new Date(activity.date) >= cutoff);"
        " }"
    )


def activity_tooltip(template: str) -> rx.Var:
    """``tooltips`` recipe: a per-day tooltip from a ``{{count}}``/``{{date}}`` template.

    Returns the full ``{ activity: { text } }`` tooltip object as a ``Var``.
    The template is JSON-encoded so quotes and special characters are safe.
    """
    encoded = json.dumps(template)
    text_fn = (
        "(activity) => "
        f"{encoded}"
        ".replaceAll('{{count}}', activity.count)"
        ".replaceAll('{{date}}', activity.date)"
    )
    return rx.Var(f"{{ activity: {{ text: {text_fn} }} }}")


def link_blocks(href_template: str) -> rx.Var:
    """``render_block`` recipe: wrap each day block in a link.

    ``href_template`` may contain a ``{{date}}`` placeholder, replaced with the
    activity's ISO date. The block element is rendered inside an anchor via
    ``React.createElement`` (React is in scope in the compiled frontend).
    """
    encoded = json.dumps(href_template)
    return rx.Var(
        "(block, activity) => React.createElement("
        "'a', "
        f"{{ href: {encoded}.replaceAll('{{{{date}}}}', activity.date) }}, "
        "block)"
    )