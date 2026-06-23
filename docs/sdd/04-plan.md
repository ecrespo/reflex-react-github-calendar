# Implementation Plan — reflex-react-github-calendar

**Status:** Approved · **Owner:** Ernesto Crespo · **Last updated:** 2026-06-23

This plan turns the PRD and architecture into ordered, verifiable phases. Each
phase has an explicit "Done when" gate. Granular tasks are in `05-tasks.md`.

## Phase 0 — Foundations  *(this commit)*

**Goal:** A buildable, documented repository skeleton on `main`.

Work:

- Repo layout matching the `reflex component init` convention.
- `pyproject.toml`, `LICENSE` (Apache-2.0), `.gitignore`, CI workflow.
- Wrapper module with all props declared (the contract from `03-component-spec.md`).
- Demo app stub with one section per feature.
- SDD docs (00–05) + research notes + README + CHANGELOG.
- Smoke tests for React wiring and prop presence.

**Done when:** `pip install -e ".[dev]"` succeeds, `pytest` collects and the
wiring tests pass, and the SDD set is complete and internally consistent.

## Phase 1 — Core wrapper

**Goal:** The basic calendar renders end-to-end in a real Reflex app.

Work:

- Verify `library`/`tag`/`is_default`/`NoSSRComponent` produce a working import.
- Confirm `username`, `year`, `error_message`, `throw_on_error` behave.
- Run the demo's "Basic calendar" section against a live frontend.

**Done when:** `github_calendar(username="grubersjoe")` renders the upstream
calendar in `reflex run`, including the loading→loaded transition.

## Phase 2 — Full feature parity

**Goal:** Every Must/Should prop is wired and demonstrated.

Work:

- Sizing (`block_size`, `block_margin`, `block_radius`, `font_size`).
- Appearance (`color_scheme`, `theme`).
- Labels/legends (`show_month_labels`, `show_weekday_labels`,
  `show_color_legend`, `show_total_count`, `labels`).
- Levels & week start (`min_level`, `max_level`, `week_start`).
- `loading` placeholder; `year` selector.

**Done when:** Each demo section visibly changes the calendar as documented, and
`03-component-spec.md` matches the implemented behavior.

## Phase 3 — Advanced props *(stretch)*

**Goal:** Ergonomic Python access to function-valued props.

Work:

- Helpers/recipes for `transform_data` (e.g. "last N days", "last half year").
- A `render_block`-based helper to wrap days in links or attach click events.
- A tooltip helper (and optional `_get_custom_code` to import the default CSS).

**Done when:** At least one helper per advanced prop is documented and shown in
the demo.

## Phase 4 — Release

**Goal:** Publish to PyPI.

Work:

- Finalize version + `CHANGELOG.md`.
- `python -m build`; validate the wheel installs in a clean venv.
- `twine upload`; tag the release; update README install instructions.

**Done when:** `pip install reflex-react-github-calendar` works from PyPI and the
demo runs against the installed package.

## Sequencing & dependencies

```
Phase 0 ──▶ Phase 1 ──▶ Phase 2 ──▶ Phase 4
                            └─▶ Phase 3 (optional, before or after 4)
```

## Definition of Done (every PR)

- Code + tests updated together.
- Affected SDD docs updated in the same PR.
- CI green (tests on 3.10–3.12, build succeeds).
