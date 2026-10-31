"""Access the game configuration data of Dragon City.

Pair it with ``dc_config_mapper`` to get the restructured/translated data.

Fan-made library, not affiliated with SocialPoint.
"""

from dc_config.config import (
    Config,
    CreateOptions,
    CreateRawOptions,
    FetchOptions,
    FetchRawOptions,
    filter_config,
)
from dc_config.dto import GameConfig, GameData, GameDataConfig
from dc_config.errors import ConfigError, ConfigHttpError
from dc_core import ConfigFilter, ConfigLanguage, ConfigPlatform

__all__ = [
    "Config",
    "ConfigError",
    "ConfigFilter",
    "ConfigHttpError",
    "ConfigLanguage",
    "ConfigPlatform",
    "CreateOptions",
    "CreateRawOptions",
    "FetchOptions",
    "FetchRawOptions",
    "GameConfig",
    "GameData",
    "GameDataConfig",
    "filter_config",
]
