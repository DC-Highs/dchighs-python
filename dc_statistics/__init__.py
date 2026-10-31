"""Generate comprehensive statistics from Dragon City configuration data.

Python port of ``@dchighs/dc-statistics``.

Fan-made library, not affiliated with SocialPoint.
"""

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional

from dc_statistics._json import as_int, as_list, get, to_camel_dict
from dc_statistics.dragons import (
    DragonCategoriesStatistics,
    DragonElementsStatistics,
    DragonsStatistics,
    generate_dragon_categories_statistics,
    generate_dragon_elements_statistics,
    generate_dragons_statistics,
)
from dc_statistics.islands import (
    IslandKindStatistics,
    IslandSections,
    IslandsStatistics,
    generate_island_kind_statistics,
    generate_islands_statistics,
    is_active_island,
    is_past_island,
    is_upcoming_island,
)
from dc_statistics.items import ItemsStatistics, generate_items_statistics


@dataclass
class GameStatistics:
    items: ItemsStatistics
    dragons: DragonsStatistics
    islands: IslandsStatistics
    max_level: int
    chests_count: int
    chest_rewards_count: int
    dragon_collections_count: int
    dragon_skins_count: int

    def to_dict(self) -> Dict[str, Any]:
        """``camelCase`` dict, the same shape the TypeScript package returns."""
        return to_camel_dict(self)


def _list_len(config: Any, section: str, key: str) -> int:
    return len(as_list(get(get(config, section), key)) or [])


def generate_statistics(config: Mapping[str, Any], now_in_seconds: Optional[int] = None) -> GameStatistics:
    """Statistics of a whole configuration.

    ``config`` can be the full document (``{"game_data": {"config": {...}}}``), the
    ``{"config": {...}}`` wrapper or the sections themselves. ``now_in_seconds`` defaults to the current time.
    """
    now = int(time.time()) if now_in_seconds is None else now_in_seconds

    section = get(get(config, "game_data"), "config")

    if section is None:
        section = get(config, "config")

    if section is None:
        section = config

    items: List[Dict[str, Any]] = [item for item in (as_list(get(section, "items")) or [])]
    dragons = [item for item in items if get(item, "group_type") == "DRAGON"]

    def islands_of(key: str) -> List[Dict[str, Any]]:
        return as_list(get(get(section, key), "islands")) or []

    island_sections = IslandSections(
        maze=islands_of("maze_island"),
        tower=islands_of("tower_island"),
        fog=islands_of("fog_island"),
        grid=islands_of("grid_island"),
        heroic_races=islands_of("heroic_races"),
        runner=islands_of("runner_island"),
        puzzle=islands_of("puzzle_island"),
    )

    levels = as_list(get(section, "levels")) or []
    max_level = (as_int(get(levels[-1], "level")) or 0) if levels else 0

    return GameStatistics(
        items=generate_items_statistics(items),
        dragons=generate_dragons_statistics(dragons),
        islands=generate_islands_statistics(island_sections, now),
        max_level=max_level,
        chests_count=_list_len(section, "chests", "chests"),
        chest_rewards_count=_list_len(section, "chests", "rewards"),
        dragon_collections_count=_list_len(section, "dragon_collections", "collections"),
        dragon_skins_count=_list_len(section, "dragon_skins", "dragon_skins"),
    )


__all__ = [
    "DragonCategoriesStatistics",
    "DragonElementsStatistics",
    "DragonsStatistics",
    "GameStatistics",
    "IslandKindStatistics",
    "IslandSections",
    "IslandsStatistics",
    "ItemsStatistics",
    "generate_dragon_categories_statistics",
    "generate_dragon_elements_statistics",
    "generate_dragons_statistics",
    "generate_island_kind_statistics",
    "generate_islands_statistics",
    "generate_items_statistics",
    "generate_statistics",
    "is_active_island",
    "is_past_island",
    "is_upcoming_island",
]
