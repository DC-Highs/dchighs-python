"""Enums shared by every DC Highs package.

String enums inherit from ``str`` so they compare equal to (and can be used as) their wire value.
"""

from enum import Enum, IntEnum
from typing import Optional, Tuple


class StringEnum(str, Enum):
    """``str`` enum whose ``str()``/format is its wire value."""

    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return format(str(self.value), format_spec)

    @property
    def as_str(self) -> str:
        return str(self.value)


class ConfigFilter(StringEnum):
    """Sections of the game configuration that can be requested/filtered."""

    CHESTS = "chests"
    ITEMS = "items"
    LEVELS = "levels"
    BREED_OPOSITE = "breed_oposite"
    TREASURE_ITEMS = "treasure_items"
    SANCTUARY_BREEDING = "sanctuary_breeding"
    HELP_VIEWS = "help_views"
    DEITY_WORLD_DRAGONS = "deity_world_dragons"
    PROGRESSIVE_ISLAND = "progressive_island"
    NEWS = "news"
    DRAGONARIUM = "dragonarium"
    GRID_ISLAND = "grid_island"
    DRAGON_BOOK = "dragon_book"
    DRAGON_TOURNAMENTS = "dragon_tournaments"
    FOG_ISLAND = "fog_island"
    HEROIC_RACES = "heroic_races"
    SPECIAL_BREEDING = "special_breeding"
    MAZE_ISLAND = "maze_island"
    TOWER_ISLAND = "tower_island"
    DRAGON_COLLECTIONS = "dragon_collections"
    EVENT_ISLAND = "event_island"
    SKILLS = "skills"
    TREE_OF_LIFE = "tree_of_life"
    TREE_OF_LIFE_RECALL = "tree_of_life_recall"
    TREE_OF_LIFE_POWERUP = "tree_of_life_powerup"
    HABITAT_TOKENS = "habitat_tokens"
    MAX_DRAGON_LEVELS = "max_dragon_levels"
    COLLECTIBLES = "collectibles"
    PUZZLE_ISLAND = "puzzle_island"
    VIP_PASS = "vip_pass"
    DRAGON_SKINS = "dragon_skins"
    DRAGON_WARS = "dragon_wars"
    FARM_CROPS = "farm_crops"
    BREEDING = "breeding"
    LIVEOPS_CHALLENGES = "liveops_challenges"
    ASSET_VERSIONING = "asset_versioning"
    BATTLE_PASS = "battle_pass"
    DRAGON_MASTERY = "dragon_mastery"
    RUNNER_ISLAND = "runner_island"
    PERKS = "perks"


class ConfigLanguage(StringEnum):
    """Languages supported by the game configuration and localization files."""

    ENGLISH = "en"
    PORTUGUESE = "pt"
    BRAZILIAN_PORTUGUESE = "br"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    JAPANESE = "ja"
    RUSSIAN = "ru"
    KOREAN = "ko"
    TURKISH = "tr"

    @classmethod
    def default(cls) -> "ConfigLanguage":
        return cls.ENGLISH


class ConfigPlatform(StringEnum):
    """Platforms the game configuration can be requested for."""

    IOS = "ios"
    ANDROID = "android"
    WINDOWS = "windows"
    AMAZON = "amazon"

    @classmethod
    def default(cls) -> "ConfigPlatform":
        return cls.IOS


class StaticFileUrlPlatformPrefix(StringEnum):
    """Sub-domain prefix of the static file servers (``{prefix}-static-s1.socialpointgames.com``)."""

    IOS = "dci"
    ANDROID = "dca"
    WINDOWS = "dcw"
    AMAZON = "dcaz"

    @classmethod
    def default(cls) -> "StaticFileUrlPlatformPrefix":
        return cls.IOS


class TextureCompressionFormat(StringEnum):
    """Texture compression format of the packaged animations/islands."""

    DXT5 = "dxt5"
    PVR = "pvr"
    ETC1 = "etc1"
    ATITC = "atitc"

    @classmethod
    def default(cls) -> "TextureCompressionFormat":
        return cls.DXT5


class SpriteQuality(StringEnum):
    """Sprite quality suffix used in the file names of the static servers.

    Shared by dragons, buildings, decorations, habitats and chests.
    """

    NORMAL = ""
    LARGE = "@2x"

    @classmethod
    def default(cls) -> "SpriteQuality":
        return cls.NORMAL


DragonSpriteQuality = SpriteQuality
BuildingSpriteQuality = SpriteQuality
DecorationSpriteQuality = SpriteQuality
HabitatSpriteQuality = SpriteQuality
ChestSpriteQuality = SpriteQuality


class IslandType(StringEnum):
    """Kinds of event islands."""

    FOG_ISLANDS = "fog_islands"
    GRID_ISLANDS = "grid_islands"
    MAZE_ISLANDS = "maze_islands"
    HEROIC_RACES = "heroic_races"
    TOWER_ISLANDS = "tower_islands"
    PUZZLE_ISLANDS = "puzzle_islands"
    RUNNER_ISLANDS = "runner_islands"
    PROGRESSIVE_ISLANDS = "progressive_islands"


class DragonElement(StringEnum):
    """Dragon elements."""

    TERRA = "terra"
    FLAME = "flame"
    SEA = "sea"
    NATURE = "nature"
    ELECTRIC = "electric"
    ICE = "ice"
    METAL = "metal"
    DARK = "dark"
    LIGHT = "light"
    WAR = "war"
    PURE = "pure"
    LEGEND = "legend"
    PRIMAL = "primal"
    WIND = "wind"
    TIME = "time"
    HAPPY = "happy"
    CHAOS = "chaos"
    MAGIC = "magic"
    SOUL = "soul"
    BEAUTY = "beauty"
    DREAM = "dream"
    PHYSICAL = "physical"

    @property
    def acronym(self) -> str:
        """Short code used by the game configuration (e.g. ``"el"`` for electric)."""
        from dc_core.settings.elements import element_info

        return element_info(self).acronym

    @classmethod
    def from_acronym(cls, acronym: str) -> Optional["DragonElement"]:
        """Resolves an element from its configuration acronym."""
        from dc_core.settings.elements import ELEMENT_INFO

        for element, info in ELEMENT_INFO.items():
            if info.acronym == acronym:
                return element
        return None

    @property
    def strengths(self) -> Tuple["DragonElement", ...]:
        from dc_core.settings.elements import element_info

        return element_info(self).strengths

    @property
    def weaknesses(self) -> Tuple["DragonElement", ...]:
        from dc_core.settings.elements import element_info

        return element_info(self).weaknesses


class DragonPhase(IntEnum):
    """Growth phase of a dragon. Its numeric value is used in asset file names."""

    EGG = 0
    BABY = 1
    YOUNG = 2
    ADULT = 3

    def __str__(self) -> str:
        return str(int(self))

    def __format__(self, format_spec: str) -> str:
        return format(int(self), format_spec)


class DragonCategory(IntEnum):
    """Dragon category / tier."""

    BASIC = 1
    PRO_BASIC = 2
    PRE_ADVANCED = 3
    ADVANCED = 4
    ELITE = 5
    AMAZING = 6
    CHARMING = 7
    GRACEFUL = 8
    CHAMPION = 9
    MYTHICAL = 10
    HEROIC = 11

    @classmethod
    def from_int(cls, value: int) -> Optional["DragonCategory"]:
        try:
            return cls(value)
        except ValueError:
            return None


class DragonRank(IntEnum):
    """Dragon battle ranks (Bronze III up to Platinum I)."""

    BRONZE_III = 1
    BRONZE_II = 2
    BRONZE_I = 3
    SILVER_III = 4
    SILVER_II = 5
    SILVER_I = 6
    GOLD_III = 7
    GOLD_II = 8
    GOLD_I = 9
    PLATINUM_III = 10
    PLATINUM_II = 11
    PLATINUM_I = 12

    @classmethod
    def from_int(cls, value: int) -> Optional["DragonRank"]:
        try:
            return cls(value)
        except ValueError:
            return None

    @property
    def name_key(self) -> str:
        from dc_core.settings.dragons import rank_name_key

        return rank_name_key(self)


class DragonRarity(StringEnum):
    """Dragon rarity (Common through Heroic)."""

    COMMON = "C"
    RARE = "R"
    VERY_RARE = "V"
    EPIC = "E"
    LEGENDARY = "L"
    MYTHIC = "M"
    HEROIC = "H"
