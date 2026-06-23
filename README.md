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

> **Status:** Phase 0 (foundations). The wrapper, demo app, full SDD docs and
> CI scaffold are in place. See [`docs/sdd/04-plan.md`](docs/sdd/04-plan.md) for
> the roadmap and current phase.

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

## Running the demo

```shell
pip install -e .
cd reflex_react_github_calendar_demo
reflex init      # first time only
reflex run
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

```shell
pip install -e ".[dev]"
pytest -q
python -m build      # produces wheel + sdist in dist/
```

CI runs the test suite on Python 3.10–3.12 and builds the distribution on every
push (see [`.github/workflows/ci.yml`](.github/workflows/ci.yml)).

## Credits & license

This package wraps [`react-github-calendar`](https://github.com/grubersjoe/react-github-calendar)
and [`react-activity-calendar`](https://github.com/grubersjoe/react-activity-calendar)
by Jonathan Gruber. Those libraries retain their own (MIT) licenses.

`reflex-react-github-calendar` is licensed under the
[Apache License 2.0](LICENSE).
