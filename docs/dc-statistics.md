# dc_statistics

Statistics of the game configuration: items, dragons, islands and general counts.
Port of `@dchighs/dc-statistics`.

Extra: `statistics` (no third-party dependencies). It works on plain dicts, so it does not even need
`dc_config`.

## `generate_statistics`

```python
from dc_statistics import generate_statistics

stats = generate_statistics(config_dict)                  # now = current time
stats = generate_statistics(config_dict, now_in_seconds=1_700_000_000)   # deterministic
```

`config_dict` may be the full document (`{"game_data": {"config": {...}}}`), `{"config": {...}}` or the sections
themselves. With `dc_config`: `generate_statistics(config.data.to_dict())`.

The result is a `GameStatistics` dataclass:

| field | content |
| --- | --- |
| `items` | `ItemsStatistics`: `total_count` and one `*_count` per `group_type` (`dragons_count`, `habitats_count`, `buildings_count`, …, 56 groups) |
| `dragons` | `DragonsStatistics` |
| `islands` | `IslandsStatistics` |
| `max_level` | `level` of the last entry of `levels` |
| `chests_count`, `chest_rewards_count`, `dragon_collections_count`, `dragon_skins_count` | sizes of those sections |

`stats.to_dict()` returns the `camelCase` shape of the TypeScript package (`maxLevel`, `chestsCount`,
`islands.heroicRaces.totalCount`, …).

## Dragons

`DragonsStatistics`: `total_count`, one count per rarity (`common_count`, `rare_count`, `very_rare_count`,
`epic_count`, `legendary_count`, `mythical_count`, `heroic_count`), `breedable_count` (`breedable == 1` or
`can_breed == 1`), `in_store_count`, `elements` and `categories`.

- `DragonElementsStatistics`: `unique_elements_count`, `dragons_with_one/two/three/four/other_elements`,
  `dragon_counts_per_element` (by element acronym).
- `DragonCategoriesStatistics`: `unique_categories_count`, `dragon_counts_per_category`.

Standalone: `generate_dragons_statistics(dragons)`, `generate_dragon_elements_statistics(dragons)`,
`generate_dragon_categories_statistics(dragons)` — `dragons` are the items whose `group_type` is `DRAGON`.

## Islands

`IslandsStatistics` has the totals (`total_count`, `actives_count`, `upcomings_count`, `pasts_count`) and one
`IslandKindStatistics` per kind: `maze`, `tower`, `fog`, `grid`, `heroic_races`, `runner`, `puzzle`.

An island is classified by `availability.from/to` or, when absent, `start_ts/end_ts` (seconds):
`is_active_island`, `is_upcoming_island`, `is_past_island`. Standalone helpers:

```python
from dc_statistics import IslandSections, generate_islands_statistics, generate_island_kind_statistics

generate_island_kind_statistics(islands, now_in_seconds=None)
generate_islands_statistics(IslandSections(maze=[...], tower=[...]), now_in_seconds=None)
```

## Items

`generate_items_statistics(items)` counts the items by `group_type`; `dc_statistics.items.GROUP_TYPES` maps every
`ItemsStatistics` field to its `group_type`.
