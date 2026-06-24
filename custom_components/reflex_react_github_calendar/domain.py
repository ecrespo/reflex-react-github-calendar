"""Domain value objects for the calendar (DDD).

These are framework-agnostic, immutable value objects that capture the upstream
invariants in Python so misconfiguration fails fast with a clear message,
instead of silently rendering a broken calendar in the browser.
"""

from __future__ import annotations

from dataclasses import dataclass

# react-activity-calendar accepts either a two-color ``[zero, max]`` scale
# (the intermediate levels are interpolated) or one explicit color per level
# (``max_level + 1`` colors; react-github-calendar forces ``max_level = 4``).
_VALID_SCALE_LENGTHS = (2, 5)


def _validate_scale(name: str, colors: list[str]) -> None:
    if len(colors) not in _VALID_SCALE_LENGTHS:
        raise ValueError(
            f"theme '{name}' scale must have 2 or 5 colors, got {len(colors)}"
        )


@dataclass(frozen=True)
class Theme:
    """A custom calendar color theme.

    ``light`` is required; ``dark`` is optional (the library falls back to the
    light scale when it is omitted). Each scale is either ``[zero, max]`` or
    five explicit per-level colors.
    """

    light: list[str]
    dark: list[str] | None = None

    def __post_init__(self) -> None:
        _validate_scale("light", self.light)
        if self.dark is not None:
            _validate_scale("dark", self.dark)

    def to_prop(self) -> dict[str, list[str]]:
        """Render the value object as the plain ``theme`` prop dict."""
        prop: dict[str, list[str]] = {"light": list(self.light)}
        if self.dark is not None:
            prop["dark"] = list(self.dark)
        return prop
