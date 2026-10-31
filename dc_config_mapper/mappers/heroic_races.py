from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dc_config_mapper.mappers.base import Mapper, MappedResult
from dc_config_mapper.schemas.heroic import (
    HeroicEncounterIn,
    HeroicEnemy,
    HeroicLapIn,
    HeroicMissionIn,
    HeroicNodeIn,
    HeroicRacesIslandIn,
    HeroicRewardIn,
)
from dc_config_mapper.utils import array, parse, passthrough


@dataclass
class MappedHeroicRaces(MappedResult):
    islands: List[Dict[str, Any]]
    rewards: List[Dict[str, Any]]
    encounters: List[Dict[str, Any]]
    enemies: List[Dict[str, Any]]
    laps: List[Dict[str, Any]]
    missions: List[Dict[str, Any]]
    nodes: List[Dict[str, Any]]
    lap_rewards: Optional[Any] = None
    nodes_position: Optional[Any] = None
    parameters: Optional[Any] = None
    spin_rewards: Optional[Any] = None


class HeroicRacesMapper(Mapper):
    """Maps ``config.heroic_races``."""

    def map(self, section: Any) -> MappedHeroicRaces:
        """``section`` is the ``heroic_races`` section."""
        return MappedHeroicRaces(
            islands=[
                self.translated(parse("heroic race island", HeroicRacesIslandIn, island).transform())
                for island in array(section, "islands")
            ],
            rewards=[
                parse("heroic race reward", HeroicRewardIn, reward).transform()
                for reward in array(section, "rewards")
            ],
            encounters=[
                parse("heroic race encounter", HeroicEncounterIn, encounter).transform()
                for encounter in array(section, "encounters")
            ],
            enemies=[
                parse("heroic race enemy", HeroicEnemy, enemy).transform()
                for enemy in array(section, "enemies")
            ],
            laps=[parse("heroic race lap", HeroicLapIn, lap).transform() for lap in array(section, "laps")],
            missions=[
                parse("heroic race mission", HeroicMissionIn, mission).transform()
                for mission in array(section, "missions")
            ],
            nodes=[parse("heroic race node", HeroicNodeIn, node).transform() for node in array(section, "nodes")],
            lap_rewards=passthrough(section, "lap_rewards"),
            nodes_position=passthrough(section, "nodes_position"),
            parameters=passthrough(section, "parameters"),
            spin_rewards=passthrough(section, "spin_rewards"),
        )
