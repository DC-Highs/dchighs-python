import math
import re
from typing import Any

from pydantic import BaseModel, ConfigDict

_INT_RE = re.compile(r"^[+-]?\d+$")
_FLOAT_RE = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")


class Strict(BaseModel):
    """Rejects unknown fields (like ``z.object().strict()``), so a game update that adds a field
    makes the mapper fail loudly instead of silently dropping data."""

    model_config = ConfigDict(extra="forbid")


class Loose(BaseModel):
    """Ignores unknown fields (like a plain ``z.object()``)."""

    model_config = ConfigDict(extra="ignore")


def dump(model: BaseModel) -> Any:
    """Plain-dict form of a (flat) model, without the fields that were not set."""
    return model.model_dump(exclude_none=True)


def coerce_number(value: Any) -> Any:
    """``z.coerce.number()`` for the values that show up in the configuration (numbers and numeric strings)."""
    if isinstance(value, bool):
        return int(value)

    if isinstance(value, (int, float)):
        return value

    if value is None:
        return 0

    if isinstance(value, str):
        trimmed = value.strip()

        if not trimmed:
            return 0

        if _INT_RE.match(trimmed):
            return int(trimmed)

        if _FLOAT_RE.match(trimmed):
            number = float(trimmed)

            if math.isfinite(number):
                return number

    raise ValueError(f"cannot coerce {value!r} to a number")


def coerce_number_list(value: Any) -> Any:
    if value is None:
        return None

    if not isinstance(value, list):
        raise ValueError("expected a list")

    return [coerce_number(item) for item in value]
