# dc_config

Fetch and hold the Dragon City game configuration. Port of `@dchighs/dc-config`.

Extra: `config` (`httpx`, `pydantic`). Requires `dc_core`.

The configuration is a very large JSON document whose shape changes with almost every game update, so each
section is kept as raw JSON and validated into your own types only on demand. Pair it with
[`dc_config_mapper`](dc-config-mapper.md) for restructured, translated data.

## Data model

```python
GameConfig                      # {"game_data": {"config": {...}}}
  .game_data.config -> GameDataConfig
  .config           -> GameDataConfig        # shortcut
  .to_dict() / GameConfig.from_dict(d) / from_json_str(s) / from_file(path)
```

`GameDataConfig` (the sections, keyed by name):

```python
config.section(ConfigFilter.ITEMS)            # raw JSON or None  (also accepts the name: "items")
config.get(ConfigFilter.ITEMS, List[dict])    # validated with pydantic (TypeAdapter); None when absent
list(config.keys())                           # sections present
ConfigFilter.ITEMS in config
```

## Fetching

Authenticated endpoint (`POST url?authToken=..&userId=..[&filter=..][&platform=..][&language=..]`):

```python
from dc_config import Config, ConfigFilter, ConfigLanguage, ConfigPlatform, FetchOptions

options = FetchOptions(
    url="https://...", user_id="123", auth_token="...",
    language=ConfigLanguage.ENGLISH, platform=ConfigPlatform.IOS,
    filter=[ConfigFilter.ITEMS, ConfigFilter.CHESTS],
)

config = await Config.create(options)      # -> Config(data, platform, language, filter)
game_config = await Config.fetch(options)  # -> GameConfig only
```

`repr(options)` never shows `auth_token`.

Public/raw file (`GET`), keeping only the requested sections (all when `filter` is empty):

```python
from dc_config import CreateRawOptions, FetchRawOptions

config = await Config.create_raw(CreateRawOptions("https://.../config.json", filter=[ConfigFilter.LEVELS]))
game_config = await Config.fetch_raw(FetchRawOptions("https://.../config.json"))
```

All fetch methods take `client=` (an `httpx.AsyncClient`). Network, HTTP-status and invalid-JSON failures raise
`ConfigHttpError` (base class `ConfigError`); a body that is not a `game_data.config` document raises `ValueError`.

`Config.language`/`platform` default to `ENGLISH`/`IOS` when not given.

## Filtering

`filter_config(game_config, filter)` keeps only the requested sections that exist.

## Working from disk

```python
game_config = GameConfig.from_file("config.json")
```
