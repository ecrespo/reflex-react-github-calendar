"""Demo Reflex app for reflex-react-github-calendar.

Reproduces every example from the upstream demo
(https://grubersjoe.github.io/react-github-calendar/) as interactive sections:

1. Basic calendar with a username switcher.
2. Sizing controls (block size / margin / radius / font size).
3. Color scheme + custom theme.
4. Label & legend toggles (month, weekday, color legend, total count).
5. Year selector.
6. Custom localization labels.
7. Loading state.
8. Advanced props via the Phase 3 helpers (transform_data + tooltips).

Run from the repo root::

    pip install -e .
    cd reflex_react_github_calendar_demo
    reflex run
"""

from __future__ import annotations

import reflex as rx

from reflex_react_github_calendar import (
    activity_tooltip,
    github_calendar,
    last_half_year,
)

DEFAULT_USERNAME = "grubersjoe"

# Example custom themes (light/dark color scales) shown in the theme section.
THEMES: dict[str, dict[str, list[str]]] = {
    "GitHub (default)": {},
    "Firebrick": {
        "light": ["#ebedf0", "#fb6a4a", "#de2d26", "#a50f15", "#67000d"],
        "dark": ["#161b22", "#fb6a4a", "#de2d26", "#a50f15", "#67000d"],
    },
    "Ocean": {
        "light": ["#eef4ff", "#9ecbff", "#4f9fff", "#1f6feb", "#0a3069"],
        "dark": ["#0d1117", "#0a3069", "#1f6feb", "#4f9fff", "#9ecbff"],
    },
}


class DemoState(rx.State):
    """All controlled values for the demo."""

    username: str = DEFAULT_USERNAME
    pending_username: str = DEFAULT_USERNAME

    # Sizing.
    block_size: int = 12
    block_margin: int = 4
    block_radius: int = 2
    font_size: int = 14

    # Appearance.
    color_scheme: str = "light"  # "light" | "dark"
    theme_name: str = "GitHub (default)"

    # Toggles.
    show_month_labels: bool = True
    show_weekday_labels: bool = False
    show_color_legend: bool = True
    show_total_count: bool = True
    loading: bool = False

    # Year selector ("last" or a specific year as string).
    year: str = "last"

    @rx.var
    def theme(self) -> dict[str, list[str]]:
        """The currently selected custom theme (empty = library default)."""
        return THEMES.get(self.theme_name, {})

    @rx.var
    def year_value(self) -> str | int:
        """Convert the year selector into the prop value ('last' or int)."""
        return self.year if self.year == "last" else int(self.year)

    def apply_username(self) -> None:
        """Commit the pending username from the input field."""
        value = self.pending_username.strip()
        if value:
            self.username = value


def section(title: str, *children: rx.Component) -> rx.Component:
    """A titled card wrapping one example."""
    return rx.card(
        rx.heading(title, size="5", margin_bottom="0.75em"),
        *children,
        width="100%",
        padding="1.5em",
    )


def example_basic() -> rx.Component:
    return section(
        "1. Basic calendar",
        rx.hstack(
            rx.input(
                placeholder="GitHub username",
                value=DemoState.pending_username,
                on_change=DemoState.set_pending_username,
            ),
            rx.button("Show calendar", on_click=DemoState.apply_username),
            spacing="2",
            margin_bottom="1em",
        ),
        github_calendar(
            username=DemoState.username,
            color_scheme=DemoState.color_scheme,
        ),
    )


def example_sizing() -> rx.Component:
    return section(
        "2. Sizing (block size / margin / radius / font size)",
        rx.vstack(
            rx.text(f"Block size: {DemoState.block_size}px"),
            rx.slider(
                min=6, max=20, default_value=12,
                on_change=DemoState.set_block_size,
            ),
            rx.text(f"Block margin: {DemoState.block_margin}px"),
            rx.slider(
                min=1, max=10, default_value=4,
                on_change=DemoState.set_block_margin,
            ),
            rx.text(f"Block radius: {DemoState.block_radius}px"),
            rx.slider(
                min=0, max=10, default_value=2,
                on_change=DemoState.set_block_radius,
            ),
            rx.text(f"Font size: {DemoState.font_size}px"),
            rx.slider(
                min=10, max=24, default_value=14,
                on_change=DemoState.set_font_size,
            ),
            spacing="2",
            margin_bottom="1em",
            width="100%",
        ),
        github_calendar(
            username=DemoState.username,
            block_size=DemoState.block_size,
            block_margin=DemoState.block_margin,
            block_radius=DemoState.block_radius,
            font_size=DemoState.font_size,
            color_scheme=DemoState.color_scheme,
        ),
    )


def example_theme() -> rx.Component:
    return section(
        "3. Color scheme & custom theme",
        rx.hstack(
            rx.select(
                ["light", "dark"],
                value=DemoState.color_scheme,
                on_change=DemoState.set_color_scheme,
            ),
            rx.select(
                list(THEMES.keys()),
                value=DemoState.theme_name,
                on_change=DemoState.set_theme_name,
            ),
            spacing="3",
            margin_bottom="1em",
        ),
        github_calendar(
            username=DemoState.username,
            color_scheme=DemoState.color_scheme,
            theme=DemoState.theme,
        ),
    )


def example_labels() -> rx.Component:
    return section(
        "4. Label & legend toggles",
        rx.hstack(
            rx.checkbox(
                "Month labels",
                checked=DemoState.show_month_labels,
                on_change=DemoState.set_show_month_labels,
            ),
            rx.checkbox(
                "Weekday labels",
                checked=DemoState.show_weekday_labels,
                on_change=DemoState.set_show_weekday_labels,
            ),
            rx.checkbox(
                "Color legend",
                checked=DemoState.show_color_legend,
                on_change=DemoState.set_show_color_legend,
            ),
            rx.checkbox(
                "Total count",
                checked=DemoState.show_total_count,
                on_change=DemoState.set_show_total_count,
            ),
            spacing="4",
            margin_bottom="1em",
            wrap="wrap",
        ),
        github_calendar(
            username=DemoState.username,
            show_month_labels=DemoState.show_month_labels,
            show_weekday_labels=DemoState.show_weekday_labels,
            show_color_legend=DemoState.show_color_legend,
            show_total_count=DemoState.show_total_count,
            color_scheme=DemoState.color_scheme,
        ),
    )


def example_year() -> rx.Component:
    return section(
        "5. Year selector",
        rx.select(
            ["last", "2024", "2023", "2022", "2021", "2020"],
            value=DemoState.year,
            on_change=DemoState.set_year,
            margin_bottom="1em",
        ),
        github_calendar(
            username=DemoState.username,
            year=DemoState.year_value,
            color_scheme=DemoState.color_scheme,
        ),
    )


def example_custom_labels() -> rx.Component:
    return section(
        "6. Custom localization labels",
        rx.text(
            "Custom totalCount string with {{count}} and {{year}} placeholders.",
            margin_bottom="1em",
            color_scheme="gray",
        ),
        github_calendar(
            username=DemoState.username,
            labels={
                "totalCount": "{{count}} contributions in {{year}}",
            },
            color_scheme=DemoState.color_scheme,
        ),
    )


def example_loading() -> rx.Component:
    return section(
        "7. Loading state",
        rx.button(
            rx.cond(DemoState.loading, "Stop loading", "Show loading state"),
            on_click=DemoState.set_loading(~DemoState.loading),
            margin_bottom="1em",
        ),
        github_calendar(
            username=DemoState.username,
            loading=DemoState.loading,
            color_scheme=DemoState.color_scheme,
        ),
    )


def example_advanced() -> rx.Component:
    return section(
        "8. Advanced props (Phase 3 helpers)",
        rx.text(
            "transform_data=last_half_year(), per-day tooltips via "
            "activity_tooltip(...), and the opt-in headless tooltip stylesheet.",
            margin_bottom="1em",
            color_scheme="gray",
        ),
        github_calendar(
            username=DemoState.username,
            color_scheme=DemoState.color_scheme,
            transform_data=last_half_year(),
            tooltips=activity_tooltip("{{count}} contributions on {{date}}"),
            show_color_legend=False,
            include_tooltip_styles=True,
        ),
    )


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("reflex-react-github-calendar", size="8"),
            rx.text(
                "A Reflex custom component wrapping react-github-calendar v5.",
                color_scheme="gray",
                margin_bottom="1em",
            ),
            example_basic(),
            example_sizing(),
            example_theme(),
            example_labels(),
            example_year(),
            example_custom_labels(),
            example_loading(),
            example_advanced(),
            spacing="5",
            width="100%",
            padding_y="2em",
        ),
        max_width="960px",
    )


app = rx.App()
app.add_page(index, title="reflex-react-github-calendar demo")
