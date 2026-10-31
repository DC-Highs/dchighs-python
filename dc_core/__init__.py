"""Shared enums, settings, tools and calculators for the DC Highs Dragon City packages.

Python port of ``@dchighs/dc-core`` (see also the Rust port).

Fan-made library, not affiliated with SocialPoint.
"""

from dc_core.calculators import *  # noqa: F401,F403
from dc_core.calculators import __all__ as _calculators_all
from dc_core.enums import (
    BuildingSpriteQuality,
    ChestSpriteQuality,
    ConfigFilter,
    ConfigLanguage,
    ConfigPlatform,
    DecorationSpriteQuality,
    DragonCategory,
    DragonElement,
    DragonPhase,
    DragonRank,
    DragonRarity,
    DragonSpriteQuality,
    HabitatSpriteQuality,
    IslandType,
    SpriteQuality,
    StaticFileUrlPlatformPrefix,
    StringEnum,
    TextureCompressionFormat,
)
from dc_core.settings import *  # noqa: F401,F403
from dc_core.settings import __all__ as _settings_all
from dc_core.tools import *  # noqa: F401,F403
from dc_core.tools import __all__ as _tools_all

__all__ = [
    *_calculators_all,
    *_settings_all,
    *_tools_all,
    "BuildingSpriteQuality",
    "ChestSpriteQuality",
    "ConfigFilter",
    "ConfigLanguage",
    "ConfigPlatform",
    "DecorationSpriteQuality",
    "DragonCategory",
    "DragonElement",
    "DragonPhase",
    "DragonRank",
    "DragonRarity",
    "DragonSpriteQuality",
    "HabitatSpriteQuality",
    "IslandType",
    "SpriteQuality",
    "StaticFileUrlPlatformPrefix",
    "StringEnum",
    "TextureCompressionFormat",
]
