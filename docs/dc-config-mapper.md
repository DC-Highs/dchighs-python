# dc_config_mapper

Validate, restructure, translate and populate the game configuration. Port of `@dchighs/dc-config-mapper`.

Extra: `config-mapper` (`httpx`, `pydantic`, `pluralizer`). Requires `dc_core` and `dc_localization`.

```python
config = await Config.create(FetchOptions(url, user_id, auth_token, filter=[ConfigFilter.CHESTS]))
localization = await Localization.create(ConfigLanguage.ENGLISH)

chests = ChestsMapper(localization).map(config.data.config.section(ConfigFilter.CHESTS))
```

## Mappers

A mapper takes the raw section and a `Localization` (share one instance between mappers). Each section is
validated against **strict** pydantic schemas: a field the schema does not know raises `SchemaError` (so a game
update that adds a field fails loudly instead of silently dropping data), and numbers must be real numbers.

| mapper | section (`ConfigFilter`) | returns |
| --- | --- | --- |
| `ChestsMapper` | `CHESTS` | `list[dict]` — reward ids resolved into reward objects |
| `ItemsMapper` | `ITEMS` | `MappedItems` — items grouped by `group_type` |
| `SkillsMapper` | `SKILLS` | `MappedSkills` |
| `HeroicRacesMapper` | `HEROIC_RACES` | `MappedHeroicRaces` |
| `MazeIslandsMapper` | `MAZE_ISLAND` | `MappedMazeIslands` |
| `TowerIslandsMapper` | `TOWER_ISLAND` | `MappedTowerIslands` |
| `GridIslandsMapper` | `GRID_ISLAND` | `MappedGridIslands` |
| `FogIslandsMapper` | `FOG_ISLAND` | `MappedFogIslands` |
| `RunnerIslandsMapper` | `RUNNER_ISLAND` | `MappedRunnerIslands` (`mission_pool` → `mission_pools`) |

What the mappers do: `img_name` → `image_name`, `0/1` → `bool`, timestamps → ISO dates
(`availability.from/to`), `zip_file` → `zip_file_name`, compact rewards (`{"g": 10}`, `{"egg": 1042}`,
`{"el_token": 3}`) → `{"type": "gold", "amount": 10}` …, prices → `{"type": "gold"|"gem", "amount": n}`, and
`*_key` fields → `name`/`type_name`/`description` through the localization.

`Mapped*` results are dataclasses: use attributes (`maze.islands`) or `to_dict()` (absent optional sections are
left out). Sections the mapper does not restructure (`parameters`, `currencies`, …) are passed through.

### Items

`MappedItems.group("habitats")`, `.dragons`, `.buildings`, `.group_keys()`, `.to_dict()`. Every known group is
present (empty if unused); unknown `group_type`s are kept under their pluralized lower-case name
(`"NEW THING"` → `new_things`). Dragons and buildings are validated and restructured; the other groups are only
translated.

## Data compiler

Resolves id references in mapped data:

- `"dragon_id": 5` → `"dragon": {...}`
- `"reward_ids": [1, 2]` → `"rewards": [{...}, {...}]`

```python
context = (
    CompileContext()
    .with_collection("laps", heroic.laps)
    .with_collection("rewards", heroic.rewards)
    .with_collection("dragons", items.dragons)
)

compiler = DataCompiler(accepted_prefixes=["basic_", "trainable_"])   # "basic_attack_ids" -> "basic_attacks"
compiled = compiler.compile(heroic.islands[0], context)
many = compiler.compile_many(heroic.islands, context)
```

The collection name is the pluralized key without its suffix. Resolved items are compiled recursively; ids
that are not found disappear from lists and become `None` for single ids; unknown collections leave the key
untouched. The input is never modified. Circular references raise `MaxDepthExceededError` (limit 128). `ids_suffix`
and `id_suffix` are configurable (`_ids`/`_id`).

## Utilities

`process_rewards(list_of_dicts)`, `process_price(gem, gold)`, `number_to_boolean`, `iso_from_ts`, `basename`,
`resolve_grid_decoration_positions(squares, decorations, board_width, board_height)`.

## Errors

All derive from `MapperError`: `SchemaError` (`.schema`, `.source`), `MissingFieldError`, `RewardNotFoundError`,
`InvalidBooleanError`, `UnexpectedPriceError`, `UnprocessedRewardsError`, `InvalidTimestampError`,
`InvalidNumberError`, `DecorationPositionMismatchError`, `InvalidContextError`, `MaxDepthExceededError`.
