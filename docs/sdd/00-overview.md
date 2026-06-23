# Overview — reflex-react-github-calendar

**Status:** Approved · **Owner:** Ernesto Crespo · **Last updated:** 2026-06-23

## 1. What we are building

`reflex-react-github-calendar` is a [Reflex](https://reflex.dev) custom component
that wraps the React library
[`react-github-calendar`](https://github.com/grubersjoe/react-github-calendar)
v5. It lets a Reflex (pure-Python) application render a GitHub-style
contributions heatmap for any GitHub username, with full control over sizing,
color themes, labels, legends and localization — without writing any JavaScript.

The package ships two things:

- a reusable, installable component (`pip install reflex-react-github-calendar`), and
- a demo Reflex app reproducing every example from the upstream demo page.

## 2. Why

Reflex developers who want a contributions calendar currently have to wrap the
React component themselves, which requires understanding Reflex's React-wrapping
model, ESM/SSR constraints, and prop name mapping. This project does that work
once, correctly, and packages it for reuse — mirroring the author's other
`reflex-*` wrappers (e.g. `reflex-react-player`).

## 3. Scope

**In scope**

- A `GitHubCalendar` component exposing all `react-github-calendar` props plus
  the inherited `react-activity-calendar` props (sizing, theme, labels, legend,
  weekday/month labels, week start, levels, loading).
- Correct ESM + no-SSR wiring so the client-side data fetch works.
- A demo app with one interactive section per feature.
- SDD documentation, README, tests, CI, and a buildable PyPI package.

**Out of scope (initial release)**

- A Python-side data fetcher / SSR data path (the component fetches in the
  browser, matching upstream). Documented as a future option.
- First-class ergonomic Python helpers for the function-valued props
  (`transform_data`, `render_block`, `render_color_legend`, function-based
  `tooltips`). These are declared and usable via raw JS `Var`s; ergonomic
  wrappers are a Phase 3 stretch goal.

## 4. Success criteria

- `import reflex_react_github_calendar` works and `github_calendar(username=...)`
  renders the upstream calendar in a Reflex app.
- The demo app runs (`reflex run`) and every example section renders.
- `pytest` passes and `python -m build` produces a wheel + sdist.
- All public props are documented in `03-component-spec.md`.

## 5. Phase plan

| Phase | Goal | Done when |
| ----- | ---- | --------- |
| **0 — Foundations** | Repo, packaging, docs, CI scaffold | Repo builds, tests collect, SDD complete |
| **1 — Core wrapper** | `GitHubCalendar` with all simple/scalar props | Basic calendar renders in the demo |
| **2 — Full feature parity** | Theme, labels, legends, weekday/month, levels, year, loading | All demo sections work |
| **3 — Advanced props (stretch)** | Ergonomic helpers for `transform_data` / render props / tooltips | Helpers documented + demoed |
| **4 — Release** | Version, changelog, build, publish to PyPI | `pip install reflex-react-github-calendar` works |

This document set is created at the end of Phase 0; Phases 1–2 are specified in
`04-plan.md` and `05-tasks.md`.
