"""Restructure and populate the Dragon City game configuration.

* ``mappers`` validate a configuration section against strict schemas, restructure it
  (``img_name`` -> ``image_name``, ``0/1`` -> ``bool``, timestamps -> ISO dates, compact rewards ->
  typed rewards, ...) and translate it with a :class:`~dc_localization.Localization`.
* :class:`DataCompiler` resolves id references (``dragon_id``, ``reward_ids``) into the referenced objects.

.. code-block:: python

    config = await Config.create(FetchOptions(url, user_id, auth_token, filter=[ConfigFilter.CHESTS]))
    localization = await Localization.create(ConfigLanguage.ENGLISH)

    chests = ChestsMapper(localization).map(config.data.config.section(ConfigFilter.CHESTS))

Fan-made library, not affiliated with SocialPoint.
"""

from dc_config_mapper.data_compiler import CompileContext, DataCompiler
from dc_config_mapper.errors import (
    DecorationPositionMismatchError,
    InvalidBooleanError,
    InvalidContextError,
    InvalidNumberError,
    InvalidTimestampError,
    MapperError,
    MaxDepthExceededError,
    MissingFieldError,
    RewardNotFoundError,
    SchemaError,
    UnexpectedPriceError,
    UnprocessedRewardsError,
)
from dc_config_mapper.mappers import *
from dc_config_mapper.mappers import __all__ as _mappers_all
from dc_config_mapper.utils import (
    Num,
    basename,
    iso_from_ts,
    number_to_boolean,
    process_price,
    process_rewards,
    resolve_grid_decoration_positions,
)
from dc_localization import Localization

__all__ = [
    *_mappers_all,
    "CompileContext",
    "DataCompiler",
    "DecorationPositionMismatchError",
    "InvalidBooleanError",
    "InvalidContextError",
    "InvalidNumberError",
    "InvalidTimestampError",
    "Localization",
    "MapperError",
    "MaxDepthExceededError",
    "MissingFieldError",
    "Num",
    "RewardNotFoundError",
    "SchemaError",
    "UnexpectedPriceError",
    "UnprocessedRewardsError",
    "basename",
    "iso_from_ts",
    "number_to_boolean",
    "process_price",
    "process_rewards",
    "resolve_grid_decoration_positions",
]
