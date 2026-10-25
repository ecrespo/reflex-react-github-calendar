# reflex-react-github-calendar

A [Reflex](https://reflex.dev) custom component that wraps
[`react-github-calendar`](https://github.com/grubersjoe/react-github-calendar)
v5 — a GitHub-style contributions heatmap — so you can drop it into a pure-Python
Reflex app in one line.

```python
import reflex as rx
from reflex_react_github_calendar import github_calendar

def index() -> rx.Component:
    return github_calendar(username="grubersjoe")
```

[![PyPI](https://img.shields.io/pypi/v/reflex-react-github-calendar)](https://pypi.org/project/reflex-react-github-calendar/)
[![CI](https://github.com/ecrespo/reflex-react-github-calendar/actions/workflows/ci.yml/badge.svg)](https://github.com/ecrespo/reflex-react-github-calendar/actions/workflows/ci.yml)

> **Status:** Published on PyPI. Version **0.2.0** targets **Reflex 0.10**
> (Python ≥ 3.11). The wrapper, demo app, full SDD docs, the DDD `Theme` value
> object and the advanced function-prop recipes are in place. See
> [`docs/sdd/04-plan.md`](docs/sdd/04-plan.md) for the roadmap.

## Requirements

| Package version | Reflex | Python |
| --- | --- | --- |
| 0.2.x | ≥ 0.10 | ≥ 3.11 |
| 0.1.x | 0.8 – 0.9 | ≥ 3.10 |

## Features

- One-line GitHub contributions calendar for any username.
- Full prop parity with `react-github-calendar` v5 **and** its underlying
  `react-activity-calendar`: sizing, color scheme, custom themes, month/weekday
  labels, color legend, total count, activity levels, week start, localization,
  year selection, and a loading state.
- Handles the tricky parts for you: ESM-only package, **named** export, and the
  client-side data fetch (rendered as a no-SSR component).
- A demo app with one interactive section per feature.

## Installation

```shell
# From PyPI:
pip install reflex-react-github-calendar
# or
uv add reflex-react-github-calendar

# From source (development):
git clone https://github.com/ecrespo/reflex-react-github-calendar
cd reflex-react-github-calendar
uv sync
```

Reflex installs the underlying npm package (`react-github-calendar@5.0.6`) into
your app's frontend automatically on first run.

## Usage

```python
import reflex as rx
from reflex_react_github_calendar import github_calendar

class State(rx.State):
    username: str = "grubersjoe"

def index() -> rx.Component:
    return github_calendar(
        username=State.username,
        year=2024,
        block_size=14,
        color_scheme="dark",
        show_weekday_labels=["mon", "wed", "fri"],
        labels={"totalCount": "{{count}} contributions in {{year}}"},
        theme={"light": ["#eee", "firebrick"], "dark": ["#333", "#d610ae"]},
    )

app = rx.App()
app.add_page(index)
```

See the full prop reference in
[`docs/sdd/03-component-spec.md`](docs/sdd/03-component-spec.md).

### Advanced helpers (no JavaScript required)

The advanced props (`transform_data`, `tooltips`, `render_block`) take JS
functions. Pure-Python helpers build them for you:

```python
from reflex_react_github_calendar import (
    github_calendar, Theme, last_half_year, activity_tooltip, link_blocks,
)

github_calendar(
    username="grubersjoe",
    theme=Theme(light=["#eee", "firebrick"]).to_prop(),  # validated value object
    transform_data=last_half_year(),                      # last 6 months only
    tooltips=activity_tooltip("{{count}} contributions on {{date}}"),
    render_block=link_blocks("https://github.com/grubersjoe?tab=overview"),
    include_tooltip_styles=True,                          # opt-in headless CSS
)
```

`Theme` validates the color scale at construction (2 or 5 colors) so
misconfiguration fails fast in Python instead of silently breaking in the
browser. See [`docs/sdd/03-component-spec.md`](docs/sdd/03-component-spec.md) §6.

## Running the demo

```shell
uv sync                 # installs Reflex 0.10 + the component (editable)
cd reflex_react_github_calendar_demo
uv run reflex run
```

The demo needs Node.js (Reflex 0.10 works with Node 24). `uv run reflex compile`
checks that the demo compiles without starting the servers.

Open http://localhost:3000. The demo reproduces every upstream example: a basic
calendar with a username switcher, sizing controls, color scheme + custom
themes, label/legend toggles, a year selector, custom localization, and the
loading state.

## How it works

`react-github-calendar` fetches a user's contribution data in the browser from
`github-contributions-api.jogruber.de` and renders an SVG heatmap. This wrapper
maps its React surface to a Reflex component:

- subclasses `NoSSRComponent` (the data fetch is client-side),
- uses the v5 **named** export (`is_default = False`),
- pins the npm version for reproducible builds, and
- exposes every prop in idiomatic Python snake_case.

Full design rationale is in
[`docs/sdd/02-architecture.md`](docs/sdd/02-architecture.md).

## Documentation

Spec-Driven Design artifacts live in [`docs/sdd/`](docs/sdd):

| Doc | Purpose |
| --- | ------- |
| [`00-overview.md`](docs/sdd/00-overview.md) | Project framing & phase plan |
| [`01-prd.md`](docs/sdd/01-prd.md) | Product requirements |
| [`02-architecture.md`](docs/sdd/02-architecture.md) | Technical design & ADRs |
| [`03-component-spec.md`](docs/sdd/03-component-spec.md) | The API contract |
| [`04-plan.md`](docs/sdd/04-plan.md) | Implementation plan |
| [`05-tasks.md`](docs/sdd/05-tasks.md) | Task breakdown |

Research notes are in [`docs/research/`](docs/research).

## Development

This project uses [uv](https://docs.astral.sh/uv/) as its package manager.

```shell
uv sync                       # create .venv, install the package (editable) + dev group
uv run pytest                 # run the test suite
uv build                      # build wheel + sdist (generates the .pyi stubs)
```

The package uses the `src/` layout of the official
[Reflex component template](https://github.com/reflex-dev/component-template).
The `.pyi` type stubs are generated at build time by the `hatch-reflex-pyi`
hook and are not committed (Reflex 0.10 removed `reflex component build`).

CI ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) runs on GitHub
Actions with the Node 24 runtime: the test suite on Python 3.11–3.14, a
distribution build that checks the wheel ships the stubs, and a compile of the
demo app.

## Publishing (Reflex custom component)

This package follows the
[Reflex custom-component](https://reflex.dev/docs/wrapping-react/overview/)
conventions and carries the `reflex-custom-components` keyword so it is
discoverable on PyPI.

Releases are published by
[`.github/workflows/publish.yml`](.github/workflows/publish.yml) through
[PyPI trusted publishing](https://docs.pypi.org/trusted-publishers/) — no API
token is stored in the repository.

**One-time setup:** on PyPI, add a trusted publisher for
`ecrespo/reflex-react-github-calendar` with workflow `publish.yml` and
environment `pypi`, and create the `pypi` environment in the GitHub repository
settings.

**Release a new version:**

1. Bump `version` in `pyproject.toml` and `__version__` in
   `src/reflex_react_github_calendar/__init__.py`, update `CHANGELOG.md`, and
   run `uv lock`.
2. Open a PR to `main` and merge it once CI is green.
3. Tag the merge commit on `main` and push the tag:

   ```shell
   git checkout main && git pull
   git tag v0.2.0
   git push origin v0.2.0
   ```

The workflow checks that the tag matches the `pyproject.toml` version and is on
`main`, runs the tests, builds the wheel + sdist (with stubs), uploads them to
PyPI and creates the GitHub release.

## Credits & license

This package wraps [`react-github-calendar`](https://github.com/grubersjoe/react-github-calendar)
and [`react-activity-calendar`](https://github.com/grubersjoe/react-activity-calendar)
by Jonathan Gruber. Those libraries retain their own (MIT) licenses.

`reflex-react-github-calendar` is licensed under the
[Apache License 2.0](LICENSE).
