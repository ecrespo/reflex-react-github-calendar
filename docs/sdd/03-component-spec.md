# Component Specification — reflex-react-github-calendar

**Status:** Approved · **Owner:** Ernesto Crespo · **Last updated:** 2026-06-23
**Audience:** Consumers of the component and contributors maintaining the API.

This is the API contract. Behavioral changes must update this document in the
same pull request.

## 1. Public API

```python
from reflex_react_github_calendar import github_calendar, GitHubCalendar
from reflex_react_github_calendar import REACT_GITHUB_CALENDAR_VERSION

github_calendar(username="grubersjoe")   # factory (preferred)
GitHubCalendar.create(username="grubersjoe")  # equivalent
```

- `github_calendar` — convenience factory (`GitHubCalendar.create`).
- `GitHubCalendar` — the component class (`NoSSRComponent` subclass).
- `REACT_GITHUB_CALENDAR_VERSION` — the pinned npm version string.

## 2. Props

All prop names are Python snake_case; Reflex converts them to the React
camelCase name shown in the "React prop" column. Defaults are those of the
underlying React component (we do not set our own).

### 2.1 react-github-calendar props

| Python prop | React prop | Type | Default | Description |
| ----------- | ---------- | ---- | ------- | ----------- |
| `username` | `username` | `str` | — (required) | GitHub username to display. |
| `year` | `year` | `int \| "last"` | `"last"` | Year to display, or the trailing 12 months. |
| `error_message` | `errorMessage` | `str` | auto | Message shown when the fetch fails (if not throwing). |
| `throw_on_error` | `throwOnError` | `bool` | `False` | Raise instead of rendering an error message. |

### 2.2 react-activity-calendar props (via composition)

| Python prop | React prop | Type | Default | Description |
| ----------- | ---------- | ---- | ------- | ----------- |
| `block_margin` | `blockMargin` | `int` | `4` | Margin between day blocks (px). |
| `block_radius` | `blockRadius` | `int` | `2` | Corner radius of day blocks (px). |
| `block_size` | `blockSize` | `int` | `12` | Size of each day block (px). |
| `color_scheme` | `colorScheme` | `"light" \| "dark"` | system | Force a color scheme. |
| `font_size` | `fontSize` | `int` | `14` | Label font size (px). |
| `labels` | `labels` | `dict` | — | Localization strings; `totalCount` supports `{{count}}`/`{{year}}`. |
| `max_level` | `maxLevel` | `int` | `4` | Maximum activity level. |
| `min_level` | `minLevel` | `int` | `0` | Minimum activity level. |
| `loading` | `loading` | `bool` | `False` | Show the loading placeholder. |
| `show_color_legend` | `showColorLegend` | `bool` | `True` | Toggle the color legend. |
| `show_month_labels` | `showMonthLabels` | `bool` | `True` | Toggle month labels. |
| `show_total_count` | `showTotalCount` | `bool` | `True` | Toggle the total-count line. |
| `show_weekday_labels` | `showWeekdayLabels` | `bool \| list[str]` | `False` | Show weekday labels; a list selects specific days (e.g. `["mon","wed","fri"]`). |
| `theme` | `theme` | `dict` | GitHub theme | Custom color theme (see §3). |
| `week_start` | `weekStart` | `int` | `0` (Sun) | Index of the week-start day. |

Inherited from `rx.Component` and **not redeclared**: `style`, `class_name`
(`className`), `id`, and the standard CSS/layout props. Use these as usual.

### 2.3 Advanced (function-valued) props

These accept JavaScript functions and must be passed as raw `Var`s (ADR-6).
Ergonomic Python helpers are a Phase 3 goal.

| Python prop | React prop | JS signature |
| ----------- | ---------- | ------------ |
| `transform_data` | `transformData` | `(data: Activity[]) => Activity[]` |
| `render_block` | `renderBlock` | `(block: ReactElement, activity: Activity) => ReactElement` |
| `render_color_legend` | `renderColorLegend` | `(block: ReactElement, level: number) => ReactElement` |
| `tooltips` | `tooltips` | `{ activity?: { text: (a: Activity) => string }, colorLegend?: { text: (l: number) => string } }` |

`Activity` is `{ date: string; count: number; level: 0|1|2|3|4 }`.

## 3. Theme format

The `theme` prop accepts either explicit per-level colors or a `[zero, max]`
pair per scheme (a scale is interpolated). Any valid CSS color works.

```python
github_calendar(
    username="grubersjoe",
    theme={
        "light": ["#eee", "firebrick"],          # 2-color scale
        "dark": ["#333", "#5b8b39", "#9be9a8", "#40c463", "#216e39"],  # explicit
    },
)
```

If `theme` is omitted, the GitHub green theme is used. `color_scheme` forces
which scheme (light/dark) is applied regardless of system preference.

## 4. Usage examples

**Basic**

```python
import reflex as rx
from reflex_react_github_calendar import github_calendar

def index() -> rx.Component:
    return github_calendar(username="grubersjoe")
```

**Customized**

```python
github_calendar(
    username="torvalds",
    year=2024,
    block_size=14,
    block_margin=5,
    color_scheme="dark",
    show_weekday_labels=["mon", "wed", "fri"],
    labels={"totalCount": "{{count}} contributions in {{year}}"},
)
```

**Advanced (raw JS Var) — last 90 days only**

```python
github_calendar(
    username="grubersjoe",
    transform_data=rx.Var.create("(data) => data.slice(-90)"),
    show_color_legend=False,
)
```

## 5. Compatibility & contract notes

- Wraps `react-github-calendar@5.0.6` (pinned). v5 is ESM-only and uses a
  **named** export.
- v4→v5 renames apply: use `show_color_legend` (not `hide_color_legend`) and
  `show_month_labels` (not `hide_month_labels`).
- The component is client-only (no SSR) and fetches data at runtime; expect a
  brief loading state on first paint.
