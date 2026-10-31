from dc_statistics import (
    IslandSections,
    generate_dragon_categories_statistics,
    generate_dragon_elements_statistics,
    generate_dragons_statistics,
    generate_island_kind_statistics,
    generate_islands_statistics,
    generate_items_statistics,
    generate_statistics,
    is_active_island,
    is_past_island,
    is_upcoming_island,
)


def test_dragon_statistics_ignore_malformed_data():
    dragons = [
        {"dragon_rarity": 5, "attributes": "f", "category": "1"},
        {"dragon_rarity": "X", "attributes": ["f", 3, "e", "d", "c", "l"], "category": -1},
        {"dragon_rarity": "R", "attributes": ["f", "e", "d"], "category": 2, "breedable": True, "in_store": 1.0},
        {"dragon_rarity": "V", "attributes": ["f"], "category": 2},
        {"dragon_rarity": "E"},
        {"dragon_rarity": "L"},
        {"dragon_rarity": "M"},
        "not a dict",
    ]

    stats = generate_dragons_statistics(dragons)

    assert stats.total_count == 8
    assert (stats.rare_count, stats.very_rare_count, stats.epic_count, stats.legendary_count) == (1, 1, 1, 1)
    assert stats.mythical_count == 1 and stats.common_count == 0 and stats.heroic_count == 0
    assert stats.breedable_count == 0 and stats.in_store_count == 0
    assert stats.elements.dragons_with_one_element == 1
    assert stats.elements.dragons_with_three_elements == 1
    assert stats.elements.dragons_with_other_elements == 6
    assert stats.categories.dragon_counts_per_category == {2: 2}
    assert stats.to_dict()["categories"]["uniqueCategoriesCount"] == 1
    assert stats.elements.to_dict()["dragonsWithThreeElements"] == 1
    assert generate_dragon_elements_statistics(dragons).unique_elements_count == 5
    assert generate_dragon_categories_statistics([{"category": 3}]).to_dict() == {
        "uniqueCategoriesCount": 1,
        "dragonCountsPerCategory": {3: 1},
    }


def test_island_classification_fallbacks():
    now = 100

    assert is_active_island({"availability": {"from": 50, "to": 150}}, now)
    assert not is_active_island({"availability": {"from": 50}}, now)
    assert is_active_island({"availability": {"from": 50}, "start_ts": 10, "end_ts": 200}, now)
    assert not is_active_island({"start_ts": 10}, now)
    assert not is_active_island({}, now)

    assert is_upcoming_island({"availability": {"from": 150}}, now)
    assert is_upcoming_island({"availability": {"to": 150}, "start_ts": 200}, now)
    assert not is_upcoming_island({"end_ts": 5}, now)

    assert is_past_island({"availability": {"to": 50}}, now)
    assert is_past_island({"availability": {"from": 1}, "end_ts": 50}, now)
    assert not is_past_island({"start_ts": 1}, now)


def test_island_statistics_defaults_to_the_current_time():
    far_future = {"start_ts": 4_000_000_000, "end_ts": 4_100_000_000}
    kind = generate_island_kind_statistics([far_future])
    assert (kind.total_count, kind.upcomings_count) == (1, 1)
    assert kind.to_dict()["upcomingsCount"] == 1

    islands = generate_islands_statistics(IslandSections(maze=[far_future], fog=[{"start_ts": 1, "end_ts": 2}]))
    assert (islands.upcomings_count, islands.pasts_count, islands.total_count) == (1, 1, 2)
    assert islands.to_dict()["fog"]["pastsCount"] == 1


def test_items_statistics_skip_items_without_group():
    stats = generate_items_statistics([{"group_type": "DRAGON"}, {"group_type": 3}, {}, "x"])

    assert (stats.total_count, stats.dragons_count) == (4, 1)
    assert stats.to_dict()["dragonsCount"] == 1


def test_config_wrappers_and_missing_sections():
    wrapped = {"config": {"items": [{"group_type": "DRAGON"}], "levels": [{"level": 7}]}}

    assert generate_statistics(wrapped).dragons.total_count == 1
    assert generate_statistics(wrapped["config"]).max_level == 7
    assert generate_statistics({"game_data": {}, "items": []}).items.total_count == 0
    assert generate_statistics({"levels": [{}]}).max_level == 0
    assert generate_statistics({}).chests_count == 0
