from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dc_config_mapper.mappers.base import Mapper, MappedResult
from dc_config_mapper.schemas.fog import FogIslandIn, FogRewardIn, FogSquareIn
from dc_config_mapper.utils import array, ids_where, parse, passthrough, with_fields


@dataclass
class MappedFogIslands(MappedResult):
    islands: List[Dict[str, Any]]
    squares: List[Dict[str, Any]]
    rewards: List[Dict[str, Any]]
    currencies: Optional[Any] = None
    actions: Optional[Any] = None
    hints: Optional[Any] = None
    parameters: Optional[Any] = None


class FogIslandsMapper(Mapper):
    """Maps ``config.fog_island``."""

    def map(self, section: Any) -> MappedFogIslands:
        """``section`` is the ``fog_island`` section."""
        squares = array(section, "squares")
        islands = []

        for island in array(section, "islands"):
            square_ids = ids_where(squares, "island_id", island)
            parsed = parse("fog island", FogIslandIn, with_fields(island, square_ids=square_ids))
            islands.append(self.translated(parsed.transform()))

        return MappedFogIslands(
            islands=islands,
            squares=[parse("fog island square", FogSquareIn, square).transform() for square in squares],
            rewards=[
                parse("fog island reward", FogRewardIn, reward).transform()
                for reward in array(section, "rewards")
            ],
            currencies=passthrough(section, "currencies"),
            actions=passthrough(section, "actions"),
            hints=passthrough(section, "hints"),
            parameters=passthrough(section, "parameters"),
        )
