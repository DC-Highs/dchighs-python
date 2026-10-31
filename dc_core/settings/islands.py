from typing import Tuple

from dc_core.enums import IslandType

ALL_ISLAND_TYPES: Tuple[IslandType, ...] = (
    IslandType.FOG_ISLANDS,
    IslandType.GRID_ISLANDS,
    IslandType.MAZE_ISLANDS,
    IslandType.HEROIC_RACES,
    IslandType.TOWER_ISLANDS,
    IslandType.PUZZLE_ISLANDS,
    IslandType.RUNNER_ISLANDS,
    IslandType.PROGRESSIVE_ISLANDS,
)
