# Product Requirements — reflex-react-github-calendar

**Status:** Approved · **Owner:** Ernesto Crespo · **Last updated:** 2026-06-23
**Audience:** Anyone deciding *what* the component must do and *why*.

## 1. Problem statement

Reflex apps are written entirely in Python and compile to React. There is no
native Reflex component for a GitHub contributions calendar. Developers must
hand-wrap `react-github-calendar`, which involves non-obvious details (ESM-only
package, client-side data fetch, no-SSR requirement, prop-name mapping). We want
a turnkey, well-documented component so a Reflex developer can add a
contributions calendar in one line.

## 2. Users & use cases

- **Portfolio / resume sites** (the author maintains several): show a user's
  GitHub activity on a personal page.
- **Dashboards**: embed a team member's or org member's contribution heatmap.
- **Reflex component consumers**: install from PyPI and use without touching JS.

## 3. Goals

- G1 — One-line usage: `github_calendar(username="grubersjoe")`.
- G2 — Full prop parity with `react-github-calendar` v5 and its underlying
  `react-activity-calendar`.
- G3 — Works out of the box (handles ESM + client-side fetch + no-SSR).
- G4 — A demo app that documents every feature interactively.
- G5 — Installable, tested, CI-covered, and publishable to PyPI.

## 4. Non-goals

- N1 — Reimplementing the calendar in Python/SVG (we wrap, not rebuild).
- N2 — A server-side data-fetch / SSR path in the first release.
- N3 — Authentication or private contribution data (upstream uses a public API).

## 5. Functional requirements

| ID | Requirement | Priority |
| -- | ----------- | -------- |
| FR-1 | Render a contributions calendar for a given `username`. | Must |
| FR-2 | Support `year` as an integer or the literal `"last"`. | Must |
| FR-3 | Expose error handling: `error_message` and `throw_on_error`. | Must |
| FR-4 | Expose sizing: `block_size`, `block_margin`, `block_radius`, `font_size`. | Must |
| FR-5 | Expose `color_scheme` ("light"/"dark") and custom `theme`. | Must |
| FR-6 | Expose label/legend toggles: `show_month_labels`, `show_weekday_labels`, `show_color_legend`, `show_total_count`. | Must |
| FR-7 | Expose `labels` for localization (with `{{count}}`/`{{year}}`). | Must |
| FR-8 | Expose `min_level`, `max_level`, `week_start`. | Should |
| FR-9 | Expose a `loading` placeholder state. | Should |
| FR-10 | Allow advanced function props (`transform_data`, `render_block`, `render_color_legend`, `tooltips`) via raw JS `Var`s. | Should |
| FR-11 | Ergonomic Python helpers for advanced function props. | Could (Phase 3) |

## 6. Non-functional requirements

- NFR-1 — Pure-Python API; no JS required for the Must-have features.
- NFR-2 — Reproducible builds via a pinned npm version of the React package.
- NFR-3 — Python ≥ 3.10, Reflex ≥ 0.8.
- NFR-4 — Apache-2.0 license (matches Reflex and sibling packages).
- NFR-5 — CI on Python 3.10/3.11/3.12; build artifacts produced on every push.

## 7. Acceptance criteria

- AC-1 — In a Reflex app, `github_calendar(username="grubersjoe")` renders the
  same calendar as the upstream React component.
- AC-2 — Each Must/Should prop changes the rendered output as documented.
- AC-3 — The demo app exposes a section per feature and runs via `reflex run`.
- AC-4 — `pytest` passes; `python -m build` emits a wheel and sdist.

## 8. Risks & assumptions

- The upstream contributions API
  (`github-contributions-api.jogruber.de`) is a third-party service; outages
  affect all consumers equally. We surface this via `error_message`.
- v5 is ESM-only with a named export; getting the import style wrong is the most
  common failure mode (see Architecture ADR-2).
- Function-valued props cannot be expressed as plain Python data; they require
  JS function `Var`s, hence the phased approach for FR-10/FR-11.
