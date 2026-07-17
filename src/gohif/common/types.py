"""
Shared type aliases.
"""

from __future__ import annotations

from pathlib import Path
from typing import TypeAlias

PathLike: TypeAlias = str | Path

JSONPrimitive: TypeAlias = (
    str
    | int
    | float
    | bool
    | None
)

JSONValue: TypeAlias = (
    JSONPrimitive
    | list["JSONValue"]
    | dict[str, "JSONValue"]
)

