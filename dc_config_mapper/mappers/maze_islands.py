from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dc_config_mapper.mappers.base import Mapper, MappedResult
from dc_config_mapper.schemas.maze import MazeIslandIn, MazeNodeIn, MazePathIn
from dc_config_mapper.utils import array, parse, passthrough


@dataclass
class MappedMazeIslands(MappedResult):
    paths: List[Dict[str, Any]]
    islands: List[Dict[str, Any]]
    nodes: List[Dict[str, Any]]
    actions: Optional[Any] = None
    clouds: Optional[Any] = None
    currencies: Optional[Any] = None
    happy_hours: Optional[Any] = None
    rewards: Optional[Any] = None
    rewards_config: Optional[Any] = None
    rewards_tiers: Optional[Any] = None
    encounters: Optional[Any] = None
    enemies: Optional[Any] = None
    parameters: Optional[Any] = None


class MazeIslandsMapper(Mapper):
    """Maps ``config.maze_island``."""

    def map(self, section: Any) -> MappedMazeIslands:
        """``section`` is the ``maze_island`` section."""
        return MappedMazeIslands(
            paths=[
                self.translated(parse("maze island path", MazePathIn, path).transform())
                for path in array(section, "paths")
            ],
            islands=[
                self.translated(parse("maze island", MazeIslandIn, island).transform())
                for island in array(section, "islands")
            ],
            nodes=[
                self.translated(parse("maze island node", MazeNodeIn, node).transform())
                for node in array(section, "nodes")
            ],
            actions=passthrough(section, "actions"),
            clouds=passthrough(section, "clouds"),
            currencies=passthrough(section, "currencies"),
            happy_hours=passthrough(section, "happy_hours"),
            rewards=passthrough(section, "rewards"),
            rewards_config=passthrough(section, "rewards_config"),
            rewards_tiers=passthrough(section, "rewards_tiers"),
            encounters=passthrough(section, "encounters"),
            enemies=passthrough(section, "enemies"),
            parameters=passthrough(section, "parameters"),
        )
