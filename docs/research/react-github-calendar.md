# Research — react-github-calendar

Notes gathered while designing the wrapper. Source of truth for the upstream
behavior the component must reproduce.

## What it is

[`react-github-calendar`](https://github.com/grubersjoe/react-github-calendar)
(by Jonathan Gruber) renders a GitHub contributions heatmap. It is built on two
sibling projects by the same author:

- [`react-activity-calendar`](https://github.com/grubersjoe/react-activity-calendar)
  — the generic activity/heatmap renderer (SVG).
- [`github-contributions-api`](https://github.com/grubersjoe/github-contributions-api)
  — the public API serving a user's contribution counts.

Current version: **v5** (latest `5.0.6` at time of research). v5 is a pure-ESM
package and **removed the default export** — use the named export
`import { GitHubCalendar } from 'react-github-calendar'`.

## How it works (from `src/index.tsx`)

1. On mount it `fetch`es
   `https://github-contributions-api.jogruber.de/v4/<username>?y=<year>`.
2. While loading, it renders `<ActivityCalendar data={[]} loading />`.
3. On error it either renders `errorMessage` or rethrows (if `throwOnError`).
4. On success it transforms `data.contributions` (optionally via `transformData`)
   and renders `<ActivityCalendar data={...} theme={gitHubTheme} maxLevel={4}
   labels={{ totalCount: "..." }} {...props} />`.

Key consequence: **data is fetched client-side**, so the component is not
SSR-compatible (the README says so explicitly). For SSR you would fetch the data
server-side and use `react-activity-calendar` directly — out of scope here.

## Props (`react-github-calendar` adds these)

| Prop | Type | Default | Notes |
| ---- | ---- | ------- | ----- |
| `username` | `string` | — (required) | Whose contributions to show. |
| `year` | `number \| 'last'` | `'last'` | Specific year or trailing 12 months. |
| `errorMessage` | `string` | auto | Shown on fetch failure if not throwing. |
| `throwOnError` | `boolean` | `false` | Rethrow for an error boundary. |
| `transformData` | `(data: Activity[]) => Activity[]` | — | Manipulate contributions before render. |

Everything else is forwarded to `react-activity-calendar`.

## Props inherited from `react-activity-calendar` (from `ActivityCalendar.tsx`)

| Prop | Type | Default |
| ---- | ---- | ------- |
| `blockMargin` | `number` | `4` |
| `blockRadius` | `number` | `2` |
| `blockSize` | `number` | `12` |
| `className` | `string` | — |
| `colorScheme` | `'light' \| 'dark'` | system |
| `fontSize` | `number` | `14` |
| `labels` | `Labels` | — (`totalCount` supports `{{count}}`/`{{year}}`) |
| `maxLevel` | `number` | `4` |
| `minLevel` | `number` | `0` |
| `loading` | `boolean` | `false` |
| `renderBlock` | `(block, activity) => ReactElement` | — |
| `renderColorLegend` | `(block, level) => ReactElement` | — |
| `showColorLegend` | `boolean` | `true` |
| `showMonthLabels` | `boolean` | `true` |
| `showTotalCount` | `boolean` | `true` |
| `showWeekdayLabels` | `boolean \| DayName[]` | `false` |
| `style` | `CSSProperties` | `{}` |
| `theme` | `ThemeInput` | GitHub theme |
| `tooltips` | `{ activity?, colorLegend? }` (text fns) | — |
| `weekStart` | `0..6` | `0` (Sunday) |

`Activity = { date: string; count: number; level: number }` where `level` is in
`[minLevel, maxLevel]` (default 0–4 → five levels).

## v4 → v5 breaking changes that matter

- Default export removed → must use the named export.
- `hideColorLegend` → `showColorLegend`; `hideMonthLabels` → `showMonthLabels`
  (booleans inverted). Several `react-activity-calendar` v3 changes apply too.
- Tooltips are now "headless" (no default CSS). Import
  `react-github-calendar/styles.css` or supply your own.

## Examples shown on the official demo (`example/src/components/Docs.tsx`)

1. **Basic** — `<GitHubCalendar username={user} fontSize={16} throwOnError />`,
   with a username input that updates a query param.
2. **Component properties table** — generated from docgen of all props.
3. **Tooltips** — points to the `react-activity-calendar` Storybook; styling via
   the optional CSS or custom classes.
4. **`transformData`** — "last half year": filter contributions to the last six
   months, with `showColorLegend={false}` and a custom `labels.totalCount`.

Storybook for `react-activity-calendar` hosts the interactive examples for
themes, activity levels, weekday labels, block sizing, and tooltips.

## Implications for the Reflex wrapper

- Must be a **no-SSR** component (client-side fetch).
- Must use a **named import** (`is_default = False`).
- All scalar props map cleanly to snake_case Reflex props.
- Function props (`transformData`, `renderBlock`, `renderColorLegend`, tooltip
  `text`) need JS function `Var`s — phased.
- There are **no event-handler props**; per-day interactivity is via
  `renderBlock`.
