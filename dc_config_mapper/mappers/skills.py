from dataclasses import dataclass
from typing import Any, Dict, List

from dc_config_mapper.mappers.base import Mapper, MappedResult
from dc_config_mapper.schemas.skills import AttackIn
from dc_config_mapper.utils import array, parse


@dataclass
class MappedSkills(MappedResult):
    skills: List[Any]
    attacks: List[Dict[str, Any]]
    auras: List[Any]
    post: List[Any]
    effects: List[Any]
    passive: List[Any]
    world_skills: List[Any]
    world_effects: List[Any]
    level_based_parameters: List[Any]


class SkillsMapper(Mapper):
    """Maps ``config.skills``."""

    def map(self, section: Any) -> MappedSkills:
        """``section`` is the ``skills`` section."""
        attacks = [
            self.translated(parse("attack", AttackIn, attack).transform())
            for attack in array(section, "attacks")
        ]

        return MappedSkills(
            skills=self.translate_all(section, "skills"),
            attacks=attacks,
            auras=self.translate_all(section, "auras"),
            post=self.translate_all(section, "post"),
            effects=self.translate_all(section, "effects"),
            passive=self.translate_all(section, "passive"),
            world_skills=self.translate_all(section, "world_skills"),
            world_effects=self.translate_all(section, "world_effects"),
            level_based_parameters=self.translate_all(section, "level_based_parameters"),
        )
