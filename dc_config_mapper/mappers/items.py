from typing import Any, Dict, Iterator, List, Tuple

from pluralizer import Pluralizer

from dc_config_mapper.errors import MissingFieldError
from dc_config_mapper.mappers.base import Mapper
from dc_config_mapper.schemas.items import BuildingIn, DragonIn
from dc_config_mapper.utils import parse

GROUPS: Tuple[Tuple[str, str], ...] = (
    ("ALLIANCE_PORTAL", "alliance_portals"),
    ("BUILDING", "buildings"),
    ("BOOSTER", "boosters"),
    ("COLLECTIBLE", "collectibles"),
    ("COLLECTISLAND", "collectislands"),
    ("FARM", "farms"),
    ("HABITAT", "habitats"),
    ("ALLIANCE_RACE", "alliance_races"),
    ("CROSSPROMOTION", "crosspromotions"),
    ("ATREZZO", "atrezzos"),
    ("BRAND_DECO", "brand_decos"),
    ("BREEDING_ISLAND", "breeding_islands"),
    ("BURROW", "burrows"),
    ("CHESTCONTAINER", "chestcontainers"),
    ("COLLECTORS_HUNT", "collectors_hunts"),
    ("CUM_CALENDAR_ISLAND", "cum_calendar_islands"),
    ("DECO", "decos"),
    ("DEUSISLAND", "deusislands"),
    ("DRAGON_CINEMA", "dragon_cinemas"),
    ("DRAGON_OBSTACLE", "dragon_obstacles"),
    ("DRAGON_PETS", "dragon_pets"),
    ("DRAGON_TRAILS", "dragon_trails"),
    ("DRAGON_TV", "dragon_tvs"),
    ("DRAGONARIUM", "dragonariums"),
    ("DWPORTAL", "dwportals"),
    ("EVENT_ISLAND", "event_islands"),
    ("FOG_ISLAND", "fog_islands"),
    ("GREENHOUSE", "greenhouses"),
    ("GD_TOWER", "gd_towers"),
    ("GRID_ISLAND", "grid_islands"),
    ("HALLOWEEN_ISLAND", "halloween_islands"),
    ("HEROIC_RACE", "heroic_races"),
    ("KINDERGARTEN", "kindergartens"),
    ("LAND", "lands"),
    ("LOSTITEM", "lostitems"),
    ("MAGE_SHRINE", "mage_shrines"),
    ("MAZE_ISLAND", "maze_islands"),
    ("MEME_GENERATOR", "meme_generators"),
    ("MISTERY_EGG", "mistery_eggs"),
    ("ORB_HABITAT", "orb_habitats"),
    ("OBSTACLE", "obstacles"),
    ("OFFERWALL", "offerwalls"),
    ("POPUP", "popups"),
    ("PROGRESSIVE_ISLAND", "progressive_islands"),
    ("PROMOISLAND", "promoislands"),
    ("PROMO", "promos"),
    ("PUZZLE_ISLAND", "puzzle_islands"),
    ("RUNNER_ISLAND", "runner_islands"),
    ("SOCIAL BUILDING", "social_buildings"),
    ("TEASER_ISLAND", "teaser_islands"),
    ("TOWER_ISLAND", "tower_islands"),
    ("TRADER_ISLAND", "trader_islands"),
    ("TREE_OF_LIFE", "tree_of_lives"),
    ("UNIT", "units"),
    ("WIZARDS_CAVE", "wizards_caves"),
    ("DRAGON", "dragons"),
)

_GROUP_KEYS: Dict[str, str] = dict(GROUPS)
_pluralizer = Pluralizer()


def group_key(group_type: str) -> str:
    """Key of a group in the mapped result. Unknown group types fall back to the generic
    rule (lowercase, pluralize, spaces to underscores) so new game groups still show up."""
    known = _GROUP_KEYS.get(group_type)

    if known is not None:
        return known

    return _pluralizer.pluralize(group_type.lower(), 2, False).replace(" ", "_")


class MappedItems:
    """Result of :meth:`ItemsMapper.map`: item groups by key (``dragons``, ``buildings``, ``decos``, ...).

    Every known group is present, empty when the configuration has no item of that group.
    """

    def __init__(self, groups: Dict[str, List[Dict[str, Any]]]) -> None:
        self.groups = groups

    def group(self, key: str) -> List[Dict[str, Any]]:
        """Items of a group, e.g. ``items.group("habitats")``."""
        return self.groups.get(key, [])

    @property
    def dragons(self) -> List[Dict[str, Any]]:
        return self.group("dragons")

    @property
    def buildings(self) -> List[Dict[str, Any]]:
        return self.group("buildings")

    def group_keys(self) -> Iterator[str]:
        """Names of the groups."""
        return iter(self.groups)

    def to_dict(self) -> Dict[str, List[Dict[str, Any]]]:
        return dict(self.groups)

    def __getitem__(self, key: str) -> List[Dict[str, Any]]:
        return self.groups[key]

    def __contains__(self, key: object) -> bool:
        return key in self.groups


class ItemsMapper(Mapper):
    """Maps ``config.items``: groups the items by ``group_type`` (``"DRAGON"`` -> ``dragons``,
    ``"SOCIAL BUILDING"`` -> ``social_buildings``, ...), validates dragons and buildings and translates names."""

    def map(self, items: Any) -> MappedItems:
        """``items`` is the ``items`` section: an array of items with a ``group_type``."""
        if not isinstance(items, list):
            raise MissingFieldError("items")

        groups: Dict[str, List[Dict[str, Any]]] = {key: [] for _, key in GROUPS}

        for item in items:
            group_type = item.get("group_type") if isinstance(item, dict) else None

            if not isinstance(group_type, str):
                continue

            key = group_key(group_type)

            if key == "dragons":
                mapped = self.translated(parse("dragon", DragonIn, item).transform())
            elif key == "buildings":
                mapped = self.translated(parse("building", BuildingIn, item).transform())
            else:
                mapped = self.localization.translate(item)

            groups.setdefault(key, []).append(mapped)

        return MappedItems(groups)
