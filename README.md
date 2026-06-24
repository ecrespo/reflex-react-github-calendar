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

> **Status:** Core wrapper + Phase 3 helpers implemented (TDD/DDD) and packaged
> as a publish-ready Reflex custom component (type stub generated, `twine check`
> passing). The wrapper, demo app, full SDD docs, CI scaffold, the DDD `Theme`
> value object and the advanced function-prop recipes are in place. See
> [`docs/sdd/04-plan.md`](docs/sdd/04-plan.md) for the roadmap and current phase.

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
# From PyPI (after the first release):
pip install reflex-react-github-calendar

# From source (development):
git clone https://github.com/ecrespo/reflex-react-github-calendar
cd reflex-react-github-calendar
pip install -e ".[dev]"
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
uv venv && uv pip install -e ".[dev]"
cd reflex_react_github_calendar_demo
uv run reflex init      # first time only
uv run reflex run
```

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
uv venv                       # create .venv
uv pip install -e ".[dev]"    # editable install + dev tools (build, twine, pytest)
uv run pytest                 # run the test suite
```

CI runs the test suite on Python 3.10–3.12 and builds the distribution on every
push (see [`.github/workflows/ci.yml`](.github/workflows/ci.yml)).

## Publishing (Reflex custom component)

This package follows the
[Reflex custom-component](https://reflex.dev/docs/custom-components/overview/)
conventions, so it is publishable to PyPI and discoverable in the Reflex gallery
(`reflex-custom-components` keyword).

**Prerequisites** (see the
[publishing prerequisites](https://reflex.dev/docs/custom-components/prerequisites-for-publishing/)):
a [PyPI](https://pypi.org) account and an API token.

**Build** — generates the `.pyi` type stub and the wheel + sdist in `dist/`:

```shell
uv run reflex component build
```

**Publish** — Reflex defers the upload to your tool of choice; with uv:

```shell
uv publish --token pypi-<your-token>      # uploads dist/* to PyPI
# or, equivalently: uv run twine upload dist/*
```

Then bump `version` in `pyproject.toml` and `__init__.py` for the next release,
and optionally run `uv run reflex component share` to submit gallery details.

## Credits & license

This package wraps [`react-github-calendar`](https://github.com/grubersjoe/react-github-calendar)
and [`react-activity-calendar`](https://github.com/grubersjoe/react-activity-calendar)
by Jonathan Gruber. Those libraries retain their own (MIT) licenses.

`reflex-react-github-calendar` is licensed under the
[Apache License 2.0](LICENSE).
