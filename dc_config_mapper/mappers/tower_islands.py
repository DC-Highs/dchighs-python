from dataclasses import dataclass
from typing import Any, Dict, List

from dc_config_mapper.mappers.base import Mapper, MappedResult
from dc_config_mapper.schemas.tower import TowerFloorIn, TowerIslandIn, TowerRewardIn, TowerSquareIn
from dc_config_mapper.utils import array, ids_where, parse, with_fields


@dataclass
class MappedTowerIslands(MappedResult):
    islands: List[Dict[str, Any]]
    floors: List[Dict[str, Any]]
    squares: List[Dict[str, Any]]
    rewards: List[Dict[str, Any]]
    happy_hours: List[Any]
    parameters: List[Any]
    currencies: List[Any]
    actions: List[Any]


class TowerIslandsMapper(Mapper):
    """Maps ``config.tower_island``."""

    def map(self, section: Any) -> MappedTowerIslands:
        """``section`` is the ``tower_island`` section."""
        squares = array(section, "squares")
        floors = array(section, "floors")
        rewards = array(section, "rewards")

        islands = []

        for island in array(section, "islands"):
            injected = with_fields(
                island,
                square_ids=ids_where(squares, "island_id", island),
                floor_ids=ids_where(floors, "island_id", island),
                reward_ids=ids_where(rewards, "island_id", island),
            )
            islands.append(self.translated(parse("tower island", TowerIslandIn, injected).transform()))

        return MappedTowerIslands(
            islands=islands,
            floors=[
                self.translated(parse("tower island floor", TowerFloorIn, floor).transform()) for floor in floors
            ],
            squares=[
                self.translated(parse("tower island square", TowerSquareIn, square).transform())
                for square in squares
            ],
            rewards=[
                self.translated(parse("tower island reward", TowerRewardIn, reward).transform())
                for reward in rewards
            ],
            happy_hours=self.translate_all(section, "happy_hours"),
            parameters=self.translate_all(section, "parameters"),
            currencies=self.translate_all(section, "currencies"),
            actions=self.translate_all(section, "actions"),
        )
