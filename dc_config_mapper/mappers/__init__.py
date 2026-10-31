"""One mapper per configuration section.

Each takes the raw section (e.g. ``config.config.section(ConfigFilter.CHESTS)``), validates it against
the strict schemas, restructures it and translates names/descriptions with the given
:class:`~dc_localization.Localization`.
"""

from dc_config_mapper.mappers.base import MappedResult, Mapper
from dc_config_mapper.mappers.chests import ChestsMapper
from dc_config_mapper.mappers.fog_islands import FogIslandsMapper, MappedFogIslands
from dc_config_mapper.mappers.grid_islands import GridIslandsMapper, MappedGridIslands
from dc_config_mapper.mappers.heroic_races import HeroicRacesMapper, MappedHeroicRaces
from dc_config_mapper.mappers.items import GROUPS, ItemsMapper, MappedItems, group_key
from dc_config_mapper.mappers.maze_islands import MappedMazeIslands, MazeIslandsMapper
from dc_config_mapper.mappers.runner_islands import MappedRunnerIslands, RunnerIslandsMapper
from dc_config_mapper.mappers.skills import MappedSkills, SkillsMapper
from dc_config_mapper.mappers.tower_islands import MappedTowerIslands, TowerIslandsMapper

__all__ = [
    "ChestsMapper",
    "FogIslandsMapper",
    "GROUPS",
    "GridIslandsMapper",
    "HeroicRacesMapper",
    "ItemsMapper",
    "MappedFogIslands",
    "MappedGridIslands",
    "MappedHeroicRaces",
    "MappedItems",
    "MappedMazeIslands",
    "MappedResult",
    "MappedRunnerIslands",
    "MappedSkills",
    "MappedTowerIslands",
    "Mapper",
    "MazeIslandsMapper",
    "RunnerIslandsMapper",
    "SkillsMapper",
    "TowerIslandsMapper",
    "group_key",
]
