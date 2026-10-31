# dc_core

Shared enums, game settings, validation tools and calculators. Port of `@dchighs/dc-core`.
Required by every other module; no third-party dependencies.

```python
from dc_core import calculate_dragon_feed_cost, DragonElement, ConfigLanguage
```

## Enums

| enum | values |
| --- | --- |
| `ConfigFilter` | configuration sections (`CHESTS`, `ITEMS`, `HEROIC_RACES`, ... — value is the section name) |
| `ConfigLanguage` | `ENGLISH="en"`, `PORTUGUESE="pt"`, `BRAZILIAN_PORTUGUESE="br"`, `SPANISH`, `FRENCH`, `GERMAN`, `ITALIAN`, `JAPANESE`, `RUSSIAN`, `KOREAN`, `TURKISH` |
| `ConfigPlatform` | `IOS`, `ANDROID`, `WINDOWS`, `AMAZON` |
| `StaticFileUrlPlatformPrefix` | `IOS="dci"`, `ANDROID="dca"`, `WINDOWS="dcw"`, `AMAZON="dcaz"` |
| `TextureCompressionFormat` | `DXT5`, `PVR`, `ETC1`, `ATITC` |
| `SpriteQuality` | `NORMAL=""`, `LARGE="@2x"` (aliases: `DragonSpriteQuality`, `BuildingSpriteQuality`, ...) |
| `IslandType` | `FOG_ISLANDS`, `GRID_ISLANDS`, `MAZE_ISLANDS`, `HEROIC_RACES`, `TOWER_ISLANDS`, `PUZZLE_ISLANDS`, `RUNNER_ISLANDS`, `PROGRESSIVE_ISLANDS` |
| `DragonElement` | 22 elements; see below |
| `DragonRarity` | `COMMON="C"` … `HEROIC="H"` |
| `DragonPhase` (int) | `EGG=0`, `BABY=1`, `YOUNG=2`, `ADULT=3` |
| `DragonCategory` (int) | `BASIC=1` … `HEROIC=11` |
| `DragonRank` (int) | `BRONZE_III=1` … `PLATINUM_I=12` |

`ConfigLanguage`, `ConfigPlatform`, `StaticFileUrlPlatformPrefix`, `TextureCompressionFormat` and
`SpriteQuality` have a `default()` classmethod (`en`, `ios`, `dci`, `dxt5`, no suffix).

```python
ConfigLanguage("tr") is ConfigLanguage.TURKISH      # parse; raises ValueError when unknown
str(SpriteQuality.LARGE)                             # "@2x"
```

`DragonElement` carries the game data of each element:

```python
DragonElement.ELECTRIC.acronym          # "el"
DragonElement.from_acronym("el")        # DragonElement.ELECTRIC (None if unknown)
DragonElement.TERRA.strengths           # (ELECTRIC, FLAME)
DragonElement.TERRA.weaknesses          # (METAL, WAR)
DragonRank.GOLD_I.name_key              # "tid_rank_gold_i"
```

## Calculators

| function | description |
| --- | --- |
| `calculate_attack_damage(DragonAttackStats(category, level, rank, stars), attack_power)` | `AttackDamageResult(minimum, maximum, average, random)` |
| `calculate_breeding_results(parent1, parent2, config)` | list of `BreedingResultItem(dragon_id, sources, required_empower, chance)` |
| `calculate_dragon_feed_cost(initial_level, final_level)` | total food between two levels (1–70) |
| `calculate_orb_recall_gain(level, stars=None)` | orbs returned when recalling a dragon |
| `calculate_element_strengths(element)` / `_by_name(name)` | elements the given one is strong against |
| `calculate_element_weaknesses(element)` / `_by_name(name)` | elements that are strong against the given one |
| `calculate_element_resistances(element)` / `_by_name(name)` | the element's listed weaknesses (as in the original) |
| `calculate_elements_strengths(elements)` / `_by_names(names)` | unique strengths of several elements |

```python
from dc_core import *

damage = calculate_attack_damage(
    DragonAttackStats(category=DragonCategory.HEROIC, level=70, rank=DragonRank.PLATINUM_I, stars=5), 1000.0
)
print(damage.minimum, damage.maximum, damage.average, damage.random)

results = calculate_breeding_results(
    {"id": 1, "elements": ["f"], "level": 20},
    {"id": 2, "elements": ["e"], "level": 20},
    breeding_config_dict,          # or a BreedingConfig; parents may be BreedingParent too
)
for item in results:
    print(item.dragon_id, [s.value for s in item.sources], item.required_empower, item.chance)
```

`BreedingSource` is `SOULMATE`, `SPECIAL`, `SANCTUARY` or `REGULAR`. The config mirrors the game data:
`breeding` (rules with `element_one`, `element_two`, `dragon_id_1..7`, `empower_1..7`), `incompatibilities`,
`soulmates`, `special_breeding` and `sanctuary_unlocked_dragons`; `BreedingConfig.from_dict` builds it from JSON.

## Validation

All validators raise a subclass of `dc_core.ValidationError` (itself a `ValueError`):

`validate_dragon_level`, `validate_dragon_stars`, `validate_dragon_level_compatibility_with_stars`,
`validate_dragon_category`, `validate_dragon_rank` (`0` → `None`), `validate_dragon_rarity(rarity, use_lower_case=False)`,
`validate_element_name`.

Subclasses: `LevelTooLowError`, `LevelTooHighError`, `StarsTooLowError`, `StarsTooHighError`,
`LevelTooHighForZeroStarsError`, `LevelTooLowForEmpowermentError`, `StarsExceedStagesError`,
`LevelTooHighForStarsError`, `InvalidCategoryError`, `InvalidRankError`, `InvalidRarityError`,
`InvalidElementError`, and `InitialLevelHigherThanFinalError` (feed cost).

## Tools

```python
parsed = DragonStaticFileUrlParser.parse_from_sprite(
    "https://dci-static-s1.socialpointgames.com/dragoncity/mobile/ui/dragons/ui_1000_dragon_terra_0@2x.png"
)
parsed.platform_prefix   # StaticFileUrlPlatformPrefix.IOS
parsed.id                # 1000
parsed.image_name        # "1000_dragon_terra"
parsed.phase             # DragonPhase.EGG
parsed.image_quality     # SpriteQuality.LARGE

get_music_name_from_tag("labyrinth_island_2015")   # "150_dc_music_labyrinth_island_2015"
```

`DragonStaticFileUrlParser` also has `parse_from_thumbnail`, `parse_from_flash_animation`,
`parse_from_spine_animation` and the individual `get_*` helpers.

## Settings

Static game data: `FEED_COST_SETTINGS`, `ORB_RECALL_PER_LEVELS`, `ORB_RECALL_PER_STARS`, `EMPOWERMENT_STAGES`,
`MINIMUM_LEVEL`/`MAXIMUM_LEVEL`/`MAXIMUM_STARS`…, `ELEMENT_INFO`, `MUSIC_KEY_NAMES`, `ALL_ISLAND_TYPES`,
plus `category_power`, `rank_power` and `rank_bonus_from_int`.
