from dataclasses import dataclass
from typing import Any, Dict, Iterable

from dc_statistics._json import as_str, get, to_camel_dict


@dataclass
class ItemsStatistics:
    total_count: int
    dragons_count: int
    habitats_count: int
    buildings_count: int
    obstacles_count: int
    decorations_count: int
    farms_count: int
    lands_count: int
    boosters_count: int
    chest_containers_count: int
    collectibles_count: int
    kindergartens_count: int
    mage_shrines_count: int
    trees_of_life_count: int
    social_buildings_count: int
    dragon_tvs_count: int
    dragonariums_count: int
    breeding_islands_count: int
    units_count: int
    lost_items_count: int
    alliance_portals_count: int
    alliance_races_count: int
    atrezzos_count: int
    brand_decos_count: int
    burrows_count: int
    collect_islands_count: int
    collectors_hunts_count: int
    cross_promotions_count: int
    cum_calendar_islands_count: int
    deus_islands_count: int
    dragon_cinemas_count: int
    dragon_obstacles_count: int
    dragon_pets_count: int
    dragon_trails_count: int
    dw_portals_count: int
    event_islands_count: int
    fog_islands_count: int
    gdtowers_count: int
    greenhouses_count: int
    grid_islands_count: int
    halloween_islands_count: int
    heroic_races_count: int
    maze_islands_count: int
    meme_generators_count: int
    mistery_eggs_count: int
    orb_habitats_count: int
    offerwalls_count: int
    popups_count: int
    progressive_islands_count: int
    promos_count: int
    promo_islands_count: int
    puzzle_islands_count: int
    runner_islands_count: int
    teaser_islands_count: int
    tower_islands_count: int
    trader_islands_count: int
    wizards_caves_count: int

    def to_dict(self) -> Dict[str, Any]:
        return to_camel_dict(self)


GROUP_TYPES: Dict[str, str] = {
    "dragons_count": "DRAGON",
    "habitats_count": "HABITAT",
    "buildings_count": "BUILDING",
    "obstacles_count": "OBSTACLE",
    "decorations_count": "DECO",
    "farms_count": "FARM",
    "lands_count": "LAND",
    "boosters_count": "BOOSTER",
    "chest_containers_count": "CHESTCONTAINER",
    "collectibles_count": "COLLECTIBLE",
    "kindergartens_count": "KINDERGARTEN",
    "mage_shrines_count": "MAGE_SHRINE",
    "trees_of_life_count": "TREE_OF_LIFE",
    "social_buildings_count": "SOCIAL BUILDING",
    "dragon_tvs_count": "DRAGON_TV",
    "dragonariums_count": "DRAGONARIUM",
    "breeding_islands_count": "BREEDING_ISLAND",
    "units_count": "UNIT",
    "lost_items_count": "LOSTITEM",
    "alliance_portals_count": "ALLIANCE_PORTAL",
    "alliance_races_count": "ALLIANCE_RACE",
    "atrezzos_count": "ATREZZO",
    "brand_decos_count": "BRAND_DECO",
    "burrows_count": "BURROW",
    "collect_islands_count": "COLLECTISLAND",
    "collectors_hunts_count": "COLLECTORS_HUNT",
    "cross_promotions_count": "CROSSPROMOTION",
    "cum_calendar_islands_count": "CUM_CALENDAR_ISLAND",
    "deus_islands_count": "DEUSISLAND",
    "dragon_cinemas_count": "DRAGON_CINEMA",
    "dragon_obstacles_count": "DRAGON_OBSTACLE",
    "dragon_pets_count": "DRAGON_PETS",
    "dragon_trails_count": "DRAGON_TRAILS",
    "dw_portals_count": "DWPORTAL",
    "event_islands_count": "EVENT_ISLAND",
    "fog_islands_count": "FOG_ISLAND",
    "gdtowers_count": "GD_TOWER",
    "greenhouses_count": "GREENHOUSE",
    "grid_islands_count": "GRID_ISLAND",
    "halloween_islands_count": "HALLOWEEN_ISLAND",
    "heroic_races_count": "HEROIC_RACE",
    "maze_islands_count": "MAZE_ISLAND",
    "meme_generators_count": "MEME_GENERATOR",
    "mistery_eggs_count": "MISTERY_EGG",
    "orb_habitats_count": "ORB_HABITAT",
    "offerwalls_count": "OFFERWALL",
    "popups_count": "POPUP",
    "progressive_islands_count": "PROGRESSIVE_ISLAND",
    "promos_count": "PROMO",
    "promo_islands_count": "PROMOISLAND",
    "puzzle_islands_count": "PUZZLE_ISLAND",
    "runner_islands_count": "RUNNER_ISLAND",
    "teaser_islands_count": "TEASER_ISLAND",
    "tower_islands_count": "TOWER_ISLAND",
    "trader_islands_count": "TRADER_ISLAND",
    "wizards_caves_count": "WIZARDS_CAVE",
}


def generate_items_statistics(items: Iterable[Dict[str, Any]]) -> ItemsStatistics:
    """Counts the items of each ``group_type``."""
    items = list(items)
    group_counts: Dict[str, int] = {}

    for item in items:
        group_type = as_str(get(item, "group_type"))

        if group_type is not None:
            group_counts[group_type] = group_counts.get(group_type, 0) + 1

    return ItemsStatistics(
        total_count=len(items),
        **{field: group_counts.get(group, 0) for field, group in GROUP_TYPES.items()},
    )
