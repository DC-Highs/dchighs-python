from dc_statistics import generate_statistics


def test_matches_typescript_mock_test():
    mock_config = {
        "game_data": {
            "config": {
                "items": [
                    {"group_type": "DRAGON", "dragon_rarity": "C", "attributes": ["f", "e"], "in_store": 1, "breedable": 1, "category": 1},
                    {"group_type": "DRAGON", "dragon_rarity": "H", "attributes": ["l", "li", "d", "c"], "in_store": 0, "can_breed": 1, "category": 10},
                    {"group_type": "HABITAT"},
                    {"group_type": "HABITAT"},
                    {"group_type": "BUILDING"},
                ],
                "maze_island": {"islands": [{"start_ts": 1, "end_ts": 9999999999}]},
                "tower_island": {"islands": []},
                "fog_island": {"islands": []},
                "grid_island": {"islands": []},
                "heroic_races": {"islands": []},
                "runner_island": {"islands": []},
                "puzzle_island": {"islands": []},
                "levels": [{"level": 1}, {"level": 2}],
                "chests": {"chests": [{}, {}, {}], "rewards": []},
                "dragon_collections": {"collections": [{}]},
                "dragon_skins": {"dragon_skins": [{}]},
            }
        }
    }

    stats = generate_statistics(mock_config)

    assert stats.items.total_count == 5
    assert stats.items.dragons_count == 2
    assert stats.items.habitats_count == 2
    assert stats.items.buildings_count == 1
    assert stats.items.obstacles_count == 0

    assert stats.dragons.total_count == 2
    assert stats.dragons.common_count == 1
    assert stats.dragons.heroic_count == 1
    assert stats.dragons.rare_count == 0
    assert stats.dragons.in_store_count == 1
    assert stats.dragons.breedable_count == 2

    assert stats.dragons.elements.unique_elements_count == 6
    assert stats.dragons.elements.dragons_with_two_elements == 1
    assert stats.dragons.elements.dragons_with_four_elements == 1
    assert stats.dragons.elements.dragons_with_one_element == 0
    assert stats.dragons.elements.dragon_counts_per_element["f"] == 1
    assert stats.dragons.elements.dragon_counts_per_element["d"] == 1

    assert stats.dragons.categories.unique_categories_count == 2
    assert stats.dragons.categories.dragon_counts_per_category[1] == 1
    assert stats.dragons.categories.dragon_counts_per_category[10] == 1

    assert stats.islands.total_count == 1
    assert stats.islands.actives_count == 1
    assert stats.islands.pasts_count == 0
    assert stats.islands.maze.total_count == 1
    assert stats.islands.maze.actives_count == 1
    assert stats.islands.tower.total_count == 0

    assert stats.max_level == 2
    assert stats.chests_count == 3
    assert stats.dragon_collections_count == 1
    assert stats.dragon_skins_count == 1


def test_islands_are_classified_by_time_and_output_is_camel_case():
    config = {
        "maze_island": {
            "islands": [
                {"availability": {"from": 10, "to": 20}},
                {"start_ts": 30, "end_ts": 40},
                {"start_ts": 1, "end_ts": 5},
            ]
        }
    }

    stats = generate_statistics(config, now_in_seconds=15)

    assert (stats.islands.actives_count, stats.islands.upcomings_count, stats.islands.pasts_count) == (1, 1, 1)

    data = stats.to_dict()
    assert data["islands"]["heroicRaces"]["totalCount"] == 0
    assert data["items"]["chestContainersCount"] == 0
    assert data["maxLevel"] == 0
