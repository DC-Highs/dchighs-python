import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Type, TypeVar, Union

from pydantic import TypeAdapter

from dc_core import ConfigFilter

T = TypeVar("T")


@dataclass
class GameDataConfig:
    """The configuration sections (``items``, ``chests``, ``heroic_races``, ...), keyed by name.

    The configuration is a very large JSON document whose shape changes with almost every game
    update, so each section is kept as raw JSON and typed access is offered on demand (:meth:`get`).
    """

    sections: Dict[str, Any] = field(default_factory=dict)

    def section(self, name: Union[ConfigFilter, str]) -> Optional[Any]:
        """Raw JSON of a section (by filter or name), if present."""
        return self.sections.get(str(name))

    def get(self, name: Union[ConfigFilter, str], type_: Optional[Type[T]] = None) -> Optional[T]:
        """A section, optionally validated into your own type (anything pydantic understands).

        Returns ``None`` when the section is not part of the configuration.
        """
        value = self.section(name)

        if value is None or type_ is None:
            return value

        return TypeAdapter(type_).validate_python(value)

    def keys(self) -> Iterator[str]:
        """Names of the sections that are present."""
        return iter(self.sections)

    def __contains__(self, name: object) -> bool:
        return str(name) in self.sections

    def __len__(self) -> int:
        return len(self.sections)


@dataclass
class GameData:
    config: GameDataConfig = field(default_factory=GameDataConfig)


@dataclass
class GameConfig:
    """Root of the configuration document: ``{ "game_data": { "config": { ... } } }``."""

    game_data: GameData = field(default_factory=GameData)

    @property
    def config(self) -> GameDataConfig:
        return self.game_data.config

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameConfig":
        try:
            sections = data["game_data"]["config"]
        except (KeyError, TypeError) as error:
            raise ValueError("expected a `{ game_data: { config: {...} } }` document") from error

        if not isinstance(sections, dict):
            raise ValueError("`game_data.config` must be an object")

        return cls(GameData(GameDataConfig(dict(sections))))

    def to_dict(self) -> Dict[str, Any]:
        return {"game_data": {"config": dict(self.game_data.config.sections)}}

    @classmethod
    def from_json_str(cls, text: str) -> "GameConfig":
        """Parses a configuration JSON text (for example one saved on disk)."""
        return cls.from_dict(json.loads(text))

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> "GameConfig":
        """Reads and parses a configuration JSON file."""
        return cls.from_json_str(Path(path).read_text(encoding="utf-8"))
