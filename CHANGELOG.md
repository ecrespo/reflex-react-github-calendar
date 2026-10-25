# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-10-25

Migration to **Reflex 0.10**. The component API is unchanged.

### Changed
- **Breaking:** requires Reflex ≥ 0.10 and Python ≥ 3.11 (Reflex 0.10 dropped
  Python 3.10).
- Moved the package from `custom_components/` to the `src/` layout of the
  official [Reflex component template](https://github.com/reflex-dev/component-template).
- Build backend switched from setuptools to hatchling with the
  `hatch-reflex-pyi` hook, which generates the `.pyi` stubs during `uv build`
  (Reflex 0.10 removed `reflex component build`). Stubs are no longer committed.
- Dev tooling uses a uv `dev` dependency group (`uv sync`) instead of the
  `[dev]` extra; `build`/`twine` are no longer needed.
- Demo `rxconfig.py` enables `RadixThemesPlugin` explicitly (implicit Radix
  enablement is deprecated).
- CI runs on Python 3.11–3.14 with GitHub Actions on the Node 24 runtime
  (`actions/checkout@v7`, `actions/setup-node@v7` with Node 24,
  `astral-sh/setup-uv`, `actions/upload-artifact@v7`), verifies the wheel ships
  the stubs and compiles the demo app.

### Added
- `py.typed` marker.
- `publish.yml` workflow: pushing a `vX.Y.Z` tag on `main` builds, publishes to
  PyPI via trusted publishing and creates the GitHub release.

## [0.1.0] - 2026-06-23

First release, published to PyPI: <https://pypi.org/project/reflex-react-github-calendar/0.1.0/>.
Install with `pip install reflex-react-github-calendar` (or `uv add ...`).

### Added (Packaging — Reflex custom component, publish-ready)
- Generated `github_calendar.pyi` type stub (via `reflex component build`) so
  consumers get full IDE autocomplete and type checking; shipped in the wheel.
- `uv`-based developer and publishing workflow documented in the README
  (`uv run reflex component build` → `uv publish`); `twine check` passes on the
  built wheel and sdist.
- Demo `rxconfig.py` aligned with Reflex 0.9 (Sitemap + TailwindV4 plugins).

### Added (Phase 3 — Advanced props, via TDD/DDD)
- `Theme` DDD value object (`domain.py`) validating custom color scales
  (`[zero, max]` pair or five explicit colors) and producing the `theme` prop.
- Function-prop recipes (`recipes.py`): `last_n_days(n)`, `last_half_year()`,
  `activity_tooltip(template)`, `link_blocks(href_template)` — building the
  raw JS `Var`s for `transform_data`, `tooltips` and `render_block`.
- Opt-in tooltip stylesheet via
  `github_calendar(..., include_tooltip_styles=True)` (`_get_custom_code`).
- Contract render tests locking the snake_case→camelCase mapping and the v5
  named/no-SSR wiring; domain, recipe and public-API test suites.
- Top-level re-exports of `Theme` and all recipes.
- Demo section 8 showcasing the advanced helpers.

### Added (Phase 0 — Foundations)
- Repository scaffold following the Reflex custom-component layout.
- `GitHubCalendar` wrapper for `react-github-calendar@5.0.6` (no-SSR, named
  export) exposing all `react-github-calendar` and `react-activity-calendar`
  props in snake_case.
- Demo Reflex app with one interactive section per feature.
- Spec-Driven Design documentation (`docs/sdd/00`–`05`) and research notes
  (`docs/research/`).
- Smoke tests for React wiring and prop presence.
- Apache-2.0 license, `.gitignore`, and a CI workflow (tests on Python
  3.10–3.12 + distribution build).

[Unreleased]: https://github.com/ecrespo/reflex-react-github-calendar/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/ecrespo/reflex-react-github-calendar/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/ecrespo/reflex-react-github-calendar/releases/tag/v0.1.0
