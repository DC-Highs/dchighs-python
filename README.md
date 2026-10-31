# dchighs for Python

Python ports of the [DC Highs](https://github.com/DC-Highs) Dragon City libraries, in a single Poetry project.
Fan-made, not affiliated with SocialPoint.

Every module keeps the `dc_` prefix of the original packages:

| module | port of | purpose |
| --- | --- | --- |
| `dc_core` | `@dchighs/dc-core` | shared enums, game settings, validation tools and calculators |
| `dc_localization` | `@dchighs/dc-localization` | translations fetching, key lookup, compare and object translation |
| `dc_statistics` | `@dchighs/dc-statistics` | item, dragon, island and global game statistics |
| `dc_assets` | `@dchighs/dc-assets` | download sprites, thumbnails, animations, music |
| `dc_config` | `@dchighs/dc-config` | fetch/load the game configuration |
| `dc_config_mapper` | `@dchighs/dc-config-mapper` | restructure, translate and populate the configuration |
| `dc_client_state` | `@dchighs/dc-client-state` | edit the preferences and cached assets of the Windows client |

The first six are the same modules that were ported to Rust (`rust-packages`); `dc_client_state` is the
extra one. Python 3.9+.

## Installation

Only `dc_core` is required (no third-party dependencies). Every other module is opt-in through an extra:

```sh
poetry add dchighs                          # dc_core only
poetry add "dchighs[localization,assets]"   # pick modules
poetry add "dchighs[all]"                   # everything
```

Extras: `localization`, `statistics`, `assets`, `config`, `config-mapper`, `client-state`, `all`.
See [docs/](docs/README.md) for the documentation of each module.

## Usage

Network access is `async` (`httpx.AsyncClient`); pass your own client with the `client` argument for proxies,
timeouts, connection reuse, etc. Everything else is synchronous.

```python
import asyncio

from dc_assets import DragonSpriteDownloader
from dc_config import Config, ConfigFilter, FetchOptions
from dc_config_mapper import ChestsMapper, DataCompiler, CompileContext, ItemsMapper
from dc_core import (
    ConfigLanguage, DragonAttackStats, DragonCategory, DragonPhase, DragonRank, SpriteQuality,
    calculate_attack_damage, calculate_dragon_feed_cost,
)
from dc_localization import Localization
from dc_statistics import generate_statistics


async def main():
    # dc_core
    print(calculate_dragon_feed_cost(1, 70))
    print(calculate_attack_damage(DragonAttackStats(DragonCategory.HEROIC, 70, DragonRank.PLATINUM_I, 5), 1000.0))

    # dc_config + dc_localization + dc_config_mapper
    config = await Config.create(
        FetchOptions("https://...", user_id="...", auth_token="...", filter=[ConfigFilter.ITEMS, ConfigFilter.CHESTS])
    )
    localization = await Localization.create(ConfigLanguage.ENGLISH)

    items = ItemsMapper(localization).map(config.data.config.section(ConfigFilter.ITEMS))
    chests = ChestsMapper(localization).map(config.data.config.section(ConfigFilter.CHESTS))
    print(len(items.dragons), len(chests))

    # dc_statistics (works on the raw configuration)
    print(generate_statistics(config.data.to_dict()).to_dict())

    # dc_assets
    sprite = DragonSpriteDownloader("1000_dragon_nature", DragonPhase.ADULT, image_quality=SpriteQuality.LARGE)
    await sprite.download("dragon.png")


asyncio.run(main())
```

### `dc_config_mapper`

Mappers (`ChestsMapper`, `ItemsMapper`, `SkillsMapper`, `HeroicRacesMapper`, `MazeIslandsMapper`,
`TowerIslandsMapper`, `GridIslandsMapper`, `FogIslandsMapper`, `RunnerIslandsMapper`) take the raw section,
validate it against **strict** pydantic schemas (an unknown field raises `SchemaError`, so a game update that adds a
field fails loudly), restructure it and translate it. Results are plain `dict`s; the island mappers return a
dataclass with a `to_dict()`.

`DataCompiler` resolves id references using a `CompileContext`:

```python
context = CompileContext().with_collection("laps", heroic.laps).with_collection("dragons", items.dragons)
compiler = DataCompiler(accepted_prefixes=["basic_", "trainable_"])
compiled = compiler.compile(heroic.islands[0], context)   # "lap_ids": [1] -> "laps": [{...}]
```

### `dc_client_state` (Windows 10/11)

```python
from dc_client_state import AssetType, ClientState

state = ClientState()                       # finds %LOCALAPPDATA%\Packages\SocialPoint.DragonCityMobile_*
state.preferences.disable_music()
state.preferences.set_all_farm_crops(plant_id=3)
print(state.preferences.get_user_id())
state.assets.list_assets([AssetType.IMAGE])
```

## Differences from the Rust and TypeScript versions

- Enum members are `UPPER_CASE` (`ConfigLanguage.BRAZILIAN_PORTUGUESE`); string enums are `str` subclasses, so they
  compare equal to their wire value.
- `dc_statistics` returns dataclasses; call `.to_dict()` for the `camelCase` shape of the TypeScript package.
- Downloaders take their options in the constructor (`DragonSpriteDownloader(name, phase, skin="_1")`) instead of
  chained setters, and expose `url`, `urls`, `fetch()` and `download(path)`.
- `UserDefault`/`Preferences` (`dc_client_state`) are synchronous and have `set_many`/`delete_many`, which edit
  several keys with a single read/write of the XML file.

## Development

```sh
poetry install --all-extras
poetry run poe test        # run the tests
poetry run poe cov         # tests + coverage (line and branch), fails below 100%
poetry run poe cov-html    # same, with an HTML report in htmlcov/
```
