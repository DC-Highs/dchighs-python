from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dc_config_mapper.mappers.base import Mapper, MappedResult
from dc_config_mapper.schemas.grid import (
    GridDecorationIn,
    GridEncounterIn,
    GridEpisodeIn,
    GridIslandIn,
    GridSquareIn,
)
from dc_config_mapper.utils import array, ids_where, parse, passthrough, with_fields


@dataclass
class MappedGridIslands(MappedResult):
    islands: List[Dict[str, Any]]
    episodes: List[Dict[str, Any]]
    squares: List[Dict[str, Any]]
    decorations: List[Dict[str, Any]]
    encounters: List[Dict[str, Any]]
    enemies: Optional[Any] = None
    currencies: Optional[Any] = None
    actions: Optional[Any] = None
    parameters: Optional[Any] = None


class GridIslandsMapper(Mapper):
    """Maps ``config.grid_island``."""

    def map(self, section: Any) -> MappedGridIslands:
        """``section`` is the ``grid_island`` section."""
        decorations = array(section, "decorations")

        islands = [
            self.translated(parse("grid island", GridIslandIn, island).transform())
            for island in array(section, "islands")
        ]

        episodes = []

        for episode in array(section, "episodes"):
            decoration_ids = ids_where(decorations, "episode_id", episode)
            parsed = parse("grid island episode", GridEpisodeIn, with_fields(episode, decoration_ids=decoration_ids))
            episodes.append(self.translated(parsed.transform()))

        return MappedGridIslands(
            islands=islands,
            episodes=episodes,
            squares=[
                parse("grid island square", GridSquareIn, square).transform()
                for square in array(section, "squares")
            ],
            decorations=[
                parse("grid island decoration", GridDecorationIn, decoration).transform()
                for decoration in decorations
            ],
            encounters=[
                parse("grid island encounter", GridEncounterIn, encounter).transform()
                for encounter in array(section, "encounters")
            ],
            enemies=passthrough(section, "enemies"),
            currencies=passthrough(section, "currencies"),
            actions=passthrough(section, "actions"),
            parameters=passthrough(section, "parameters"),
        )
