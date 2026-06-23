# Research — Wrapping React libraries in Reflex

Notes on the Reflex mechanics used by this component.
Source: Reflex docs, "Wrapping React" and "Custom Components" sections.

## The model

Reflex apps are written in Python and compiled to a React frontend + a Python
backend. To use a React library you subclass `rx.Component` and declare:

- `library` — the npm package name (pin a version for reproducibility, e.g.
  `"react-github-calendar@5.0.6"`).
- `tag` — the React component name exported by the package.
- `alias` — optional import alias.
- `lib_dependencies` — extra npm packages the component needs.
- `is_default` — `True` for a default export, `False` for a named export.

```python
import reflex as rx

class Spline(rx.Component):
    library = "@splinetool/react-spline@4.1.0"
    lib_dependencies = ["@splinetool/runtime@1.5.5"]
    tag = "Spline"
    is_default = True          # default export
    scene: rx.Var[str]         # a prop

spline = Spline.create
```

## Props

Props are declared as class attributes annotated with `rx.Var[...]`. Reflex
automatically converts snake_case Python names to camelCase React names
(`block_size` → `blockSize`). Override with `_rename_props` only when the
heuristic would be wrong:

```python
class Page(rx.Component):
    library = "@react-pdf/renderer"
    tag = "Page"
    theme: rx.Var[dict]
    _rename_props = {"theme": "style"}   # 'style' is reserved in Reflex
```

Prop categories: **simple** (data), **callback** (functions), **component**
(children/elements), and **event handlers**.

## Event handlers

Event triggers are declared with `rx.EventHandler[spec]`, where `spec` shapes the
arguments delivered to the Python handler. Built-in specs include
`rx.event.no_args_event_spec`, `rx.event.passthrough_event_spec(T)`,
`rx.event.input_event`, and `rx.event.key_event`. Custom specs extract a
serializable payload from the browser event:

```python
class ColorPicker(rx.NoSSRComponent):
    library = "react-colorful@5.7.0"
    tag = "HexColorPicker"
    color: rx.Var[str]
    on_change: rx.EventHandler[lambda color: [color]]
```

> `react-github-calendar` has **no** event-handler props, so this component
> declares none. (Interactivity is done via the `renderBlock` render prop.)

## NoSSRComponent — for client-only libraries

Subclass `reflex.components.component.NoSSRComponent` when the library touches
`window`/`document` or fetches data in the browser. Reflex then emits a dynamic,
SSR-disabled import:

```python
from reflex.components.component import NoSSRComponent

class MyLib(NoSSRComponent):
    library = "my-library@x.y.z"
    tag = "MyComponent"
```

This is exactly what we need: `react-github-calendar` fetches contribution data
client-side, so `GitHubCalendar` is a `NoSSRComponent`.

## Custom CSS / imports

Override `_get_custom_code` to inject extra import lines (e.g. a stylesheet):

```python
class ReactFlowLib(rx.Component):
    library = "reactflow"
    def _get_custom_code(self) -> str:
        return "import 'reactflow/dist/style.css';"
```

We use this pattern (deferred to Phase 3) to optionally import the headless
tooltip styles `react-github-calendar/styles.css`.

## Packaging a reusable component

`reflex component init` scaffolds a publishable package:

```
my_component/
├── pyproject.toml            # builds the package from custom_components/
├── README.md
├── custom_components/
│   └── reflex_my_component/
│       ├── __init__.py       # re-exports the public API
│       └── my_component.py
└── my_component_demo/        # a runnable demo app
    ├── rxconfig.py
    └── requirements.txt
```

`reflex component build` (or `python -m build`) produces a wheel + sdist;
`reflex component publish` / `twine` uploads to PyPI. Add the
`reflex-custom-components` keyword for gallery discovery. This repository follows
that exact layout.
