# Architecture / Technical Design — reflex-react-github-calendar

**Status:** Approved · **Owner:** Ernesto Crespo · **Last updated:** 2026-06-23
**Audience:** Contributors implementing or reviewing the component internals.

## 1. Context

Reflex compiles Python components into a React (Next.js / React Router)
frontend and runs a Python backend that holds application state. A "custom
component" is a Python class (`rx.Component`) that declares which npm package and
React tag to emit, plus the props and events it exposes. Our job is to map the
React surface of `react-github-calendar` v5 onto Reflex's component model
correctly.

`react-github-calendar` is a thin wrapper around
[`react-activity-calendar`](https://github.com/grubersjoe/react-activity-calendar):
it fetches contribution data for a `username` from
`github-contributions-api.jogruber.de` **in the browser**, transforms it into
`{date, count, level}` activities, and passes them (together with a GitHub color
theme and a default `totalCount` label) to `ActivityCalendar`. Therefore every
`ActivityCalendar` prop except `data` is also a prop here.

## 2. High-level architecture

```
┌────────────────────────── Reflex app (Python) ───────────────────────────┐
│  State (rx.State)                                                          │
│   ├─ controlled values: username, year, block_size, color_scheme, ...      │
│   └─ computed vars: theme, year_value, ...                                 │
│                          │  props ▼                                        │
│  GitHubCalendar(NoSSRComponent)  ───────────────────────────────────────┐ │
└──────────────────────────────────────────────────────────────────────┼──┘
                                                                         │ compiles to
                                  ▼                                      │
┌────────────────────────── React frontend ───────────────────────────────┐
│  dynamic(() => import('react-github-calendar'), { ssr: false })           │
│   └─ <GitHubCalendar username=... blockSize=... theme=... />              │
│        ├─ fetch(github-contributions-api.jogruber.de/v4/<user>?y=<year>)  │
│        └─ <ActivityCalendar data=... {...props} /> → SVG heatmap           │
└───────────────────────────────────────────────────────────────────────────┘
```

The data flow is **one-directional**: Python state → props → React render.
There is no server round-trip for the calendar data; the fetch happens in the
browser. The component is effectively display-only (no event triggers in the
base feature set — see ADR-5).

## 3. Key design decisions (ADRs)

### ADR-1 — Subclass `NoSSRComponent`
**Context:** The component fetches data using the browser `fetch` API and the
underlying SVG rendering depends on client-only measurement (`isClient`).
Server-side rendering would either crash or hydrate incorrectly.
**Decision:** Subclass `reflex.components.component.NoSSRComponent`, so Reflex
emits `dynamic(() => import(...), { ssr: false })`.
**Consequences:** The calendar renders only on the client; a brief loading state
is shown first. This matches upstream guidance (the README explicitly says SSR
is *not* supported by this component).

### ADR-2 — Named import, `is_default = False`
**Context:** v5 is a pure-ESM package and **removed the default export**. The
correct usage is `import { GitHubCalendar } from 'react-github-calendar'`.
**Decision:** Set `tag = "GitHubCalendar"` and `is_default = False`.
**Consequences:** Getting this wrong (`is_default = True`) produces
`undefined` → React "Element type is invalid". This is the single most common
failure mode and is covered by `test_library_wiring`.

### ADR-3 — Pin the npm version in a module constant
**Context:** Reproducible builds require a fixed dependency version; v5
introduced breaking changes (renamed `hideColorLegend`→`showColorLegend`, etc.).
**Decision:** `REACT_GITHUB_CALENDAR_VERSION = "react-github-calendar@5.0.6"`,
referenced by `library`. Bump deliberately, noting changes in the changelog.
**Consequences:** Predictable installs; upgrades are explicit and reviewable.

### ADR-4 — Rely on Reflex snake_case → camelCase conversion
**Context:** React props are camelCase (`blockSize`, `showColorLegend`,
`errorMessage`); Python prefers snake_case.
**Decision:** Declare props in snake_case and rely on Reflex's automatic
conversion. Keep `_rename_props` empty unless a name needs an explicit hint.
**Consequences:** Idiomatic Python API. `class_name`, `style` and `id` are *not*
redeclared — they are inherited from `rx.Component` and already map correctly.

### ADR-5 — No event triggers in the base feature set
**Context:** `react-activity-calendar` has no `onClick`-style callbacks. Per-day
interactivity is achieved via the `renderBlock` render prop (wrap each block in
a link or attach handlers), and tooltips via the `tooltips` prop whose `text`
fields are functions.
**Decision:** The base component is display-only. Interactivity and tooltips are
exposed through the function-valued props (`render_block`, `tooltips`), which
require JS function `Var`s.
**Consequences:** Simpler, robust core. Ergonomic Python wrappers for these are
deferred to Phase 3.

### ADR-6 — Function-valued props passed as raw `Var`s
**Context:** `transform_data`, `render_block`, `render_color_legend`, and the
`text` fields inside `tooltips` are JavaScript functions. Plain Python data
cannot represent a closure that runs in the browser.
**Decision:** Type these props as `rx.Var[Any]` so advanced users can pass a raw
JS function `Var` (e.g. `rx.Var("(d) => d.slice(-90)")`). Provide ergonomic
helpers later.
**Consequences:** Full power is available immediately for advanced users without
blocking the simple, common case.

### ADR-7 — Tooltip styles are opt-in
**Context:** v5 tooltips are "headless" (no default CSS). The package ships an
optional stylesheet (`react-github-calendar/tooltips.css`).
**Decision:** Document importing the stylesheet (or supplying custom CSS) rather
than forcing it. A future helper may inject it via `_get_custom_code`.
**Consequences:** No surprise styles; consumers choose their tooltip look.

## 4. Package layout

```
reflex-react-github-calendar/
├── src/
│   └── reflex_react_github_calendar/
│       ├── __init__.py            # public API
│       ├── github_calendar.py     # the GitHubCalendar wrapper
│       ├── domain.py              # Theme value object
│       ├── recipes.py             # function-prop helpers
│       └── py.typed               # .pyi stubs are generated at build time
├── reflex_react_github_calendar_demo/
│   ├── rxconfig.py
│   ├── requirements.txt
│   └── reflex_react_github_calendar_demo/
│       └── reflex_react_github_calendar_demo.py   # demo app, one section per feature
├── tests/                        # wiring, contract, domain and recipe tests
├── docs/{sdd,research}/           # this documentation
├── pyproject.toml                 # hatchling + hatch-reflex-pyi; package from src/
└── .github/workflows/
    ├── ci.yml                     # test (3.11–3.14) + build + demo compile
    └── publish.yml                # tag vX.Y.Z → PyPI (trusted publishing)
```

This follows the official
[Reflex component template](https://github.com/reflex-dev/component-template)
(`src/` layout). Reflex 0.10 removed the `reflex component` CLI, and the
`hatch-reflex-pyi` build hook that replaces its stub generation requires `src/`.

## 5. Build & distribution

`hatchling` packages `src/reflex_react_github_calendar`. `uv build` produces a
wheel + sdist; the `hatch-reflex-pyi` build hook generates the `.pyi` type stubs
during the build (they are not committed). Releases are published to PyPI by
`.github/workflows/publish.yml` when a `vX.Y.Z` tag that matches the
`pyproject.toml` version is pushed on `main`, using PyPI trusted publishing. The npm dependency is declared by `library` and installed by Reflex into
the consuming app's `.web` directory on first run — there is no separate JS
build step in this repo.

## 6. Testing strategy

- **Wiring tests** (no browser): assert `library`, `tag`, `is_default`,
  `NoSSRComponent` subclassing, and that the documented props exist. These catch
  the highest-probability mistakes cheaply.
- **Manual / demo verification**: the demo app is the human-facing acceptance
  surface for visual props (theme, sizing, labels).
- **Phase 3**: add render tests around the function-prop helpers when built.
