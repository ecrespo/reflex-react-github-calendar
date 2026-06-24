"""A Reflex wrapper around react-github-calendar v5.

`react-github-calendar` (https://github.com/grubersjoe/react-github-calendar)
renders a GitHub-style contributions heatmap. It fetches the contribution data
for a username client-side from `github-contributions-api.jogruber.de` and draws
the calendar with the underlying `react-activity-calendar` component, so every
`react-activity-calendar` prop is supported here as well.

Public API::

    from reflex_react_github_calendar import github_calendar

    github_calendar(username="grubersjoe")
"""

from __future__ import annotations

from typing import Any, Union

import reflex as rx
from reflex.components.component import NoSSRComponent

# Pinned npm version for reproducible builds (see ADR-6). Bump deliberately.
REACT_GITHUB_CALENDAR_VERSION = "react-github-calendar@5.0.6"


class GitHubCalendar(NoSSRComponent):
    """A GitHub contributions calendar (heatmap) for a given username.

    The component is client-side only: it fetches contribution data in the
    browser, so it is wrapped as a ``NoSSRComponent`` (Reflex emits a dynamic,
    SSR-disabled import). See ``docs/sdd/02-architecture.md`` for details.
    """

    # The npm package. v5 is a pure-ESM package with a *named* export.
    library = REACT_GITHUB_CALENDAR_VERSION

    # Named export `GitHubCalendar` (v5 removed the default export).
    tag = "GitHubCalendar"
    is_default = False

    # ------------------------------------------------------------------ #
    # react-github-calendar specific props
    # ------------------------------------------------------------------ #

    # GitHub username whose contributions are displayed (required).
    username: rx.Var[str]

    # Year to display: an integer (e.g. 2024) or the literal string "last"
    # (the default — the trailing 12 months, matching GitHub's behaviour).
    year: rx.Var[Union[int, str]]

    # Message shown if fetching contribution data fails (when not throwing).
    error_message: rx.Var[str]  # -> errorMessage

    # Raise instead of rendering ``error_message`` so a React error boundary
    # can catch it.
    throw_on_error: rx.Var[bool]  # -> throwOnError

    # ------------------------------------------------------------------ #
    # react-activity-calendar props (all supported via composition)
    # ------------------------------------------------------------------ #

    # Margin between day blocks, in pixels (default 4).
    block_margin: rx.Var[int]  # -> blockMargin

    # Corner radius of day blocks, in pixels (default 2).
    block_radius: rx.Var[int]  # -> blockRadius

    # Size of each day block, in pixels (default 12).
    block_size: rx.Var[int]  # -> blockSize

    # Force a color scheme instead of using the system one.
    color_scheme: rx.Var[str]  # "light" | "dark" -> colorScheme

    # Base font size for labels, in pixels (default 14).
    font_size: rx.Var[int]  # -> fontSize

    # Localization strings. ``totalCount`` supports the ``{{count}}`` and
    # ``{{year}}`` placeholders, e.g.
    # ``{"totalCount": "{{count}} contributions in {{year}}"}``.
    labels: rx.Var[dict[str, Any]]

    # Maximum activity level (default 4). react-github-calendar forces 4.
    max_level: rx.Var[int]  # -> maxLevel

    # Minimum activity level (default 0).
    min_level: rx.Var[int]  # -> minLevel

    # Show the loading placeholder; ``data`` is ignored while true.
    loading: rx.Var[bool]

    # Toggle the color legend below the calendar (default True).
    show_color_legend: rx.Var[bool]  # -> showColorLegend

    # Toggle the month labels above the calendar (default True).
    show_month_labels: rx.Var[bool]  # -> showMonthLabels

    # Toggle the total-count line below the calendar (default True).
    show_total_count: rx.Var[bool]  # -> showTotalCount

    # Show weekday labels. Either a boolean, or a list of ISO weekday names
    # to display selectively, e.g. ``["mon", "wed", "fri"]``.
    show_weekday_labels: rx.Var[Union[bool, list[str]]]  # -> showWeekdayLabels

    # Custom color theme. Provide explicit per-level colors or a [min, max]
    # pair per scheme, e.g.
    # ``{"light": ["#eee", "firebrick"], "dark": ["#333", "#d610ae"]}``.
    theme: rx.Var[dict[str, Any]]

    # Index of the day used as the week start (0 = Sunday).
    week_start: rx.Var[int]  # -> weekStart

    # ------------------------------------------------------------------ #
    # Advanced / callback props
    # ------------------------------------------------------------------ #
    # The following props accept JavaScript functions on the React side and
    # therefore must be passed as raw function ``Var``s (see
    # docs/sdd/03-component-spec.md). They are declared here so they are
    # forward-compatible; ergonomic Python helpers are tracked in Phase 3.

    # Transform the fetched contribution list before rendering.
    # ``(data: Activity[]) => Activity[]``
    transform_data: rx.Var[Any]  # -> transformData

    # Render prop for day blocks (attach links / handlers / custom tooltips).
    # ``(block: ReactElement, activity: Activity) => ReactElement``
    render_block: rx.Var[Any]  # -> renderBlock

    # Render prop for color-legend blocks.
    render_color_legend: rx.Var[Any]  # -> renderColorLegend

    # Tooltip configuration. ``activity.text`` / ``colorLegend.text`` are
    # functions, so this generally needs a function-bearing ``Var``.
    tooltips: rx.Var[dict[str, Any]]

    # Reflex auto-converts snake_case prop names to camelCase, which covers
    # every prop above. Add entries here only for names that need an explicit
    # hint that the heuristic would get wrong.
    _rename_props: dict[str, str] = {}

    @classmethod
    def create(cls, *children, include_tooltip_styles: bool = False, **props):
        """Create the component, optionally importing the tooltip stylesheet.

        v5 tooltips are headless (ADR-7), so the bundled stylesheet is opt-in.
        Pass ``include_tooltip_styles=True`` to emit
        ``import "react-github-calendar/tooltips.css";`` once in the frontend.
        """
        component = super().create(*children, **props)
        # Stored off-band so it is not treated as a React prop / CSS style.
        object.__setattr__(
            component, "_include_tooltip_styles", include_tooltip_styles
        )
        return component

    def _get_custom_code(self) -> str | None:
        """Inject the headless-tooltip stylesheet import when opted in.

        v5.0.6 exposes the stylesheet via its ``exports`` field as
        ``./tooltips.css`` (not ``./styles.css``); using the wrong path makes
        Vite fail to resolve the import.
        """
        if getattr(self, "_include_tooltip_styles", False):
            return 'import "react-github-calendar/tooltips.css";'
        return None


# Convenience factory: ``github_calendar(username="grubersjoe")``.
github_calendar = GitHubCalendar.create
