# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/ecrespo/reflex-react-github-calendar
