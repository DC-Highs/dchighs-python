"""Tiny helpers to read loosely-typed configuration JSON the way ``serde_json::Value`` accessors do."""

from dataclasses import fields, is_dataclass
from typing import Any, Dict, List, Optional


def as_int(value: Any) -> Optional[int]:
    """``Value::as_i64``: only real integers (no bools, no floats)."""
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def as_uint(value: Any) -> Optional[int]:
    """``Value::as_u64``: non-negative integers."""
    number = as_int(value)
    return number if number is not None and number >= 0 else None


def as_str(value: Any) -> Optional[str]:
    return value if isinstance(value, str) else None


def as_list(value: Any) -> Optional[List[Any]]:
    return value if isinstance(value, list) else None


def get(value: Any, key: str) -> Any:
    return value.get(key) if isinstance(value, dict) else None


def camel_case(name: str) -> str:
    head, *rest = name.split("_")
    return head + "".join(part.capitalize() for part in rest)


def to_camel_dict(value: Any) -> Any:
    """Recursively converts statistics dataclasses into ``camelCase`` dicts (the TypeScript output)."""
    if is_dataclass(value) and not isinstance(value, type):
        return {camel_case(f.name): to_camel_dict(getattr(value, f.name)) for f in fields(value)}

    if isinstance(value, dict):
        return {key: to_camel_dict(item) for key, item in value.items()}

    if isinstance(value, list):
        return [to_camel_dict(item) for item in value]

    return value


def clone_dict(value: Dict[str, Any]) -> Dict[str, Any]:
    return dict(value)
