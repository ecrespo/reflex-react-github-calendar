# Task Breakdown — reflex-react-github-calendar

**Status:** Living · **Owner:** Ernesto Crespo · **Last updated:** 2026-06-23

Granular tasks per phase. `[x]` done, `[ ]` pending. Keep in sync with reality.

## Phase 0 — Foundations

- [x] T0.1 Create repo layout (`custom_components/`, demo app, `docs/`, `tests/`).
- [x] T0.2 `pyproject.toml` (setuptools, package from `custom_components/`).
- [x] T0.3 `LICENSE` (Apache-2.0), `.gitignore`, `.github/workflows/ci.yml`.
- [x] T0.4 Wrapper module `github_calendar.py` with all props declared.
- [x] T0.5 Public API in `__init__.py` (`github_calendar`, `GitHubCalendar`, version const).
- [x] T0.6 Demo app stub with one section per feature.
- [x] T0.7 SDD docs 00–05 + research notes.
- [x] T0.8 README.md + CHANGELOG.md.
- [x] T0.9 Smoke tests (`tests/test_github_calendar.py`).
- [x] T0.10 Initialize git, `main` branch, first commit.
- [ ] T0.11 Push to GitHub (`ecrespo/reflex-react-github-calendar`, public).

## Phase 1 — Core wrapper

- [ ] T1.1 Create a clean venv; `pip install -e ".[dev]"`; `pytest`.
- [ ] T1.2 In the demo app, `reflex init` + `reflex run`; confirm the frontend
  compiles the dynamic, no-SSR import.
- [ ] T1.3 Verify the "Basic calendar" section renders for a known username.
- [ ] T1.4 Verify error handling: bad username → `error_message`; `throw_on_error`.
- [ ] T1.5 Confirm `year` accepts `"last"` and an integer.

## Phase 2 — Full feature parity

- [ ] T2.1 Sizing props change the SVG dimensions as expected.
- [ ] T2.2 `color_scheme` forces light/dark; `theme` applies a custom scale.
- [ ] T2.3 Label/legend toggles hide/show the respective elements.
- [ ] T2.4 `labels.totalCount` renders with `{{count}}`/`{{year}}` substituted.
- [ ] T2.5 `min_level`/`max_level`/`week_start` behave per upstream.
- [ ] T2.6 `loading` shows the placeholder animation.
- [ ] T2.7 Reconcile any behavioral surprises back into `03-component-spec.md`.

## Phase 3 — Advanced props (stretch)

- [x] T3.1 `transform_data` recipe(s): `last_n_days(n)` / `last_half_year()`
  (`recipes.py`, TDD in `tests/test_recipes.py`).
- [x] T3.2 `render_block` helper `link_blocks(href_template)` wrapping days in
  links via `React.createElement` (`recipes.py`).
- [x] T3.3 Tooltip helper `activity_tooltip(template)` + opt-in default CSS
  import via `GitHubCalendar.create(include_tooltip_styles=True)` →
  `_get_custom_code` (`tests/test_tooltip_styles.py`).
- [x] T3.4 Demo section 8 + spec updates (`03-component-spec.md` §6) for the above.
- [x] T3.5 DDD `Theme` value object validating color scales (`domain.py`,
  `tests/test_domain.py`).
- [x] T3.6 Contract render tests locking snake_case→camelCase wiring
  (`tests/test_contract.py`).

> Runtime (browser) verification of the generated JS for `render_block` /
> tooltips is deferred to a live `reflex run`, consistent with the Phase 1/2
> manual tasks; the helpers are unit-tested at the generated-JS level.

## Phase 4 — Release

- [ ] T4.1 Finalize version + changelog entry.
- [ ] T4.2 `python -m build`; install the wheel in a clean venv and smoke-test.
- [ ] T4.3 `twine upload`; create a GitHub release tag.
- [ ] T4.4 Update README install instructions to the published version.

## Backlog / ideas

- Optional Python-side data fetch for SSR-friendly usage.
- Convenience presets for popular themes.
- Typed `Activity`/theme dataclasses for editor autocompletion.
