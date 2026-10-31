from dataclasses import fields, is_dataclass
from typing import Any, Dict, List

from dc_config_mapper.utils import array
from dc_localization import Localization


class Mapper:
    """Boilerplate shared by every mapper: it holds the :class:`~dc_localization.Localization`
    used to translate names and descriptions (share one instance between mappers)."""

    def __init__(self, localization: Localization) -> None:
        self.localization = localization

    def translated(self, value: Dict[str, Any]) -> Dict[str, Any]:
        """Translates the ``*_key`` fields of a normalized object."""
        return self.localization.translate(value)

    def translate_all(self, section: Any, key: str) -> List[Any]:
        """Translates every element of ``section[key]`` as is."""
        return [self.localization.translate(item) for item in array(section, key)]


class MappedResult:
    """Base of the dataclasses returned by the mappers."""

    def to_dict(self) -> Dict[str, Any]:
        """JSON-friendly dict; the optional sections that are absent are left out."""
        assert is_dataclass(self)
        return {
            field.name: getattr(self, field.name)
            for field in fields(self)
            if getattr(self, field.name) is not None
        }
