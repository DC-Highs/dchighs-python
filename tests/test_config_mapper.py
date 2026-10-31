import copy

import pytest

from dc_config_mapper import (
    ChestsMapper,
    CompileContext,
    DataCompiler,
    DecorationPositionMismatchError,
    HeroicRacesMapper,
    InvalidBooleanError,
    ItemsMapper,
    MaxDepthExceededError,
    MazeIslandsMapper,
    RewardNotFoundError,
    SchemaError,
    UnexpectedPriceError,
    UnprocessedRewardsError,
    basename,
    iso_from_ts,
    number_to_boolean,
    process_price,
    process_rewards,
    resolve_grid_decoration_positions,
)
from dc_config_mapper.mappers.items import GROUPS
from dc_core import ConfigLanguage
from dc_localization import Localization


def localization() -> Localization:
    return Localization(
        ConfigLanguage.ENGLISH,
        {
            "tid_chest_name_2": "Wooden Chest",
            "tid_chest_type_2": "Chest",
            "tid_island": "Maze",
        },
    )


def chests_section():
    return {
        "chests": [
            {
                "id": 2, "type": "CHEST", "rewards": [3, 4], "img_name": "101_wood_chest",
                "chest_name_key": "tid_chest_name_2", "type_name_key": "tid_chest_type_2",
                "level_tiers": [5, 11], "default_reward": 3, "pool_size": 5,
            }
        ],
        "rewards": [
            {"id": 3, "reward": {"resource": {"g": 100}}, "tier_multi": 1, "weight": 85},
            {"id": 4, "reward": {"eggs": [1042], "resource": {"el_token": 3}}, "tier_multi": 1, "weight": 1},
        ],
    }


def test_booleans():
    assert number_to_boolean(1) is True
    assert number_to_boolean(0) is False

    with pytest.raises(InvalidBooleanError):
        number_to_boolean(2)


def test_iso_dates_and_basenames():
    assert iso_from_ts(0) == "1970-01-01T00:00:00.000Z"
    assert iso_from_ts(1_700_000_000) == "2023-11-14T22:13:20.000Z"
    assert iso_from_ts(1.5) == "1970-01-01T00:00:01.500Z"
    assert basename("a/b/c.zip") == "c.zip"
    assert basename("c.zip") == "c.zip"


def test_prices():
    assert process_price(None, None) is None
    assert process_price(None, 10) == {"type": "gold", "amount": 10}
    assert process_price(10, None) == {"type": "gem", "amount": 10}

    with pytest.raises(UnexpectedPriceError):
        process_price(10, 10)


def test_processes_every_reward_kind():
    out = process_rewards(
        [
            {"chest": 5},
            {"egg": [1, 2]},
            {"egg": 7},
            {"g": 10},
            {"c": 3},
            {"f": 4},
            {"b": [9, 10]},
            {"ep": 6},
            {"seeds": [{"id": 1, "amount": 2}, {"id": 3, "amount": 4}]},
            {"en_runner": 2},
            {"el_token": 8},
            {"pet_food_pack.xl": 1},
            {"album_pack_aces.big": 2},
            {},
        ]
    )

    assert len(out) == 14
    assert out[0] == {"type": "chest", "chest_id": 5}
    assert out[1]["dragon_ids"] == [1, 2]
    assert out[6] == {"type": "building", "building_id": 9}
    assert out[8] == {"type": "dragon_orbs", "amount": 2, "orb_dragon_id": 1}
    assert out[11] == {"type": "habitat_token", "element": "electric", "amount": 8}
    assert out[12] == {"type": "pet_food_pack", "amount": 1, "size": "xl"}
    assert out[13] == {"type": "album_pack_aces", "amount": 2, "size": "big"}


def test_unknown_reward_is_an_error():
    with pytest.raises(UnprocessedRewardsError):
        process_rewards([{"x": 1}])


def test_grid_decorations_fill_free_cells():
    squares = [{"x": 1, "y": 1}, {"x": 2, "y": 2}]
    decorations = [{"id": 1}, {"id": 2}]
    out = resolve_grid_decoration_positions(squares, decorations, 2, 2)

    assert (out[0]["x"], out[0]["y"]) == (1, 2)
    assert (out[1]["x"], out[1]["y"]) == (2, 1)

    with pytest.raises(DecorationPositionMismatchError):
        resolve_grid_decoration_positions(squares, decorations[:1], 2, 2)


def test_chests_are_resolved_restructured_and_translated():
    chests = ChestsMapper(localization()).map(chests_section())

    assert len(chests) == 1
    chest = chests[0]

    assert chest["name"] == "Wooden Chest"
    assert chest["type_name"] == "Chest"
    assert chest["image_name"] == "101_wood_chest"
    assert chest["default_reward_id"] == 3
    assert "img_name" not in chest and "chest_name_key" not in chest

    assert chest["rewards"][0]["reward"]["resource"] == {"type": "gold", "amount": 100}
    assert chest["rewards"][1]["reward"]["eggs_ids"] == [1042]
    assert chest["rewards"][1]["reward"]["resource"] == {
        "type": "habitat_token",
        "element": "electric",
        "amount": 3,
    }


def test_schemas_are_strict():
    section = chests_section()
    section["chests"][0]["brand_new_field"] = 1

    with pytest.raises(SchemaError) as error:
        ChestsMapper(localization()).map(section)

    assert "brand_new_field" in str(error.value)


def test_missing_reward_is_reported():
    section = chests_section()
    section["chests"][0]["rewards"] = [3, 999]

    with pytest.raises(RewardNotFoundError):
        ChestsMapper(localization()).map(section)


def test_numbers_must_be_numbers():
    section = chests_section()
    section["chests"][0]["pool_size"] = True

    with pytest.raises(SchemaError):
        ChestsMapper(localization()).map(section)


def test_maze_islands_get_iso_dates_and_ids():
    section = {
        "actions": [], "clouds": [], "currencies": [], "happy_hours": [], "rewards": [],
        "rewards_config": [], "rewards_tiers": [], "encounters": [], "enemies": [], "parameters": [],
        "paths": [
            {
                "id": 1, "color": [1, 2, 3], "visibility": 1, "dragon_type": 1042, "new_badge": 1,
                "mobile_dragon_scale": 1, "mobile_dragon_offset": [0, 0], "nodes": [10, 11],
            }
        ],
        "nodes": [
            {
                "id": 10, "position": [1, 2], "cost": {"ep": 20},
                "reward": [{"g": 5}, {"b": [7, 8]}], "highlighted": True,
            }
        ],
        "islands": [
            {
                "id": 303, "tid_name": "tid_island", "name": "Maze", "availability": {"from": 0, "to": 1700000000},
                "paths": [1], "happy_hours": [], "currency_id": 303, "pool_size": 2000, "pool_time": 86400,
                "initial_points": 700, "clouds": [], "cloud_radius": 1, "dragon_radius": 1, "min_level": 7,
                "building_id": 1, "mobile_tutorial_id": 1, "tutorial_path_id": 1,
                "tutorial_initial_camera_position": [0, 0], "tutorial_initial_zoom": 1, "tutorial_final_zoom": 1,
                "zip_file": "path/to/mi_spring_b.zip", "mobile_building_position": [0, 0],
                "active_platforms": {}, "help_view_id": 1, "sound_tag": "FANTASY",
            }
        ],
    }

    maze = MazeIslandsMapper(localization()).map(section)

    assert maze.islands[0]["name"] == "Maze"
    assert maze.islands[0]["availability"]["to"] == "2023-11-14T22:13:20.000Z"
    assert maze.islands[0]["zip_file_name"] == "mi_spring_b.zip"
    assert maze.islands[0]["pool"] == {"size": 2000, "time": 86400}
    assert maze.paths[0]["has_new_badge"] is True
    assert maze.paths[0]["dragon_id"] == 1042
    assert maze.nodes[0]["cost"] == 20
    assert maze.nodes[0]["rewards"][1] == {"type": "building", "building_id": 7}
    assert maze.nodes[0]["encounter_skip_cost"] is None

    result = maze.to_dict()
    assert result["parameters"] == [] and "islands" in result


def test_heroic_enemies_are_coerced_to_numbers():
    section = {
        "islands": [], "rewards": [], "encounters": [], "laps": [], "nodes": [],
        "enemies": [
            {
                "id": 1, "dragon_ids": ["1042", 7], "handicaps": [], "view_type": "x",
                "elements_view_type": [], "cooldown": 0, "enemies": ["3"],
            }
        ],
        "missions": [
            {
                "id": 1, "type": "BREED", "goal_points": 10, "price": 1, "price_increment": 0,
                "pool_size": 4, "spawn_time": 60, "collect_chance": 1, "collect_chance_modifier": 0,
            }
        ],
    }

    heroic = HeroicRacesMapper(localization()).map(section).to_dict()

    assert heroic["enemies"][0]["dragon_ids"] == [1042, 7]
    assert heroic["enemies"][0]["enemies"] == [3]
    assert heroic["missions"][0]["spawn_time"] == {"one": 60, "all": 360}
    assert "lap_rewards" not in heroic


def test_items_are_grouped_and_unknown_groups_are_kept():
    section = [
        {"id": 1, "name": "Some Booster", "group_type": "BOOSTER"},
        {"id": 2, "name": "Social", "group_type": "SOCIAL BUILDING"},
        {"id": 3, "name": "Future", "group_type": "NEW THING"},
    ]

    items = ItemsMapper(localization()).map(section)

    assert len(items.group("boosters")) == 1
    assert len(items.group("social_buildings")) == 1
    assert len(items.group("new_things")) == 1
    assert items.dragons == []


def test_invalid_item_is_reported_with_its_schema():
    with pytest.raises(SchemaError) as error:
        ItemsMapper(localization()).map([{"id": 1, "name": "broken", "group_type": "DRAGON"}])

    assert error.value.schema == "dragon"


def test_generic_group_rule_agrees_with_the_known_groups():
    from pluralizer import Pluralizer

    pluralizer = Pluralizer()

    for group_type, key in GROUPS:
        assert pluralizer.pluralize(group_type.lower(), 2, False).replace(" ", "_") == key, group_type


def context() -> CompileContext:
    return (
        CompileContext()
        .with_collection("dragons", [{"id": 1, "name": "A", "attack_ids": [10]}, {"id": 2, "name": "B"}])
        .with_collection("attacks", [{"id": 10, "name": "Bite"}])
        .with_collection("rewards", [{"id": 7, "dragon_id": 2}, {"id": 8, "dragon_id": 1}])
    )


def test_resolves_single_ids_recursively():
    out = DataCompiler().compile({"id": 5, "reward_id": 7}, context())

    assert out == {"id": 5, "reward": {"id": 7, "dragon": {"id": 2, "name": "B"}}}


def test_resolves_id_lists_and_drops_unknown_ids():
    out = DataCompiler().compile({"reward_ids": [8, 99]}, context())

    assert out == {
        "rewards": [
            {"id": 8, "dragon": {"id": 1, "name": "A", "attacks": [{"id": 10, "name": "Bite"}]}}
        ]
    }


def test_unknown_id_becomes_none_and_unknown_collections_are_left_alone():
    compiler = DataCompiler()
    ctx = context()

    assert compiler.compile({"dragon_id": 404}, ctx) == {"dragon": None}
    assert compiler.compile({"island_id": 3}, ctx) == {"island_id": 3}
    assert compiler.compile({"dragon_id": 0}, ctx) == {"dragon_id": 0}


def test_prefixes_are_kept():
    out = DataCompiler(accepted_prefixes=["basic_", "trainable_"]).compile(
        {"basic_attack_ids": [10], "trainable_attack_ids": []}, context()
    )

    assert out == {"basic_attacks": [{"id": 10, "name": "Bite"}], "trainable_attacks": []}


def test_walks_nested_objects_and_arrays():
    data = {"list": [{"dragon_id": 1}, 3, "x"], "inner": {"attack_id": 10}}
    snapshot = copy.deepcopy(data)
    out = DataCompiler().compile(data, context())

    assert out["list"][0]["dragon"]["name"] == "A"
    assert out["list"][1] == 3
    assert out["inner"]["attack"]["name"] == "Bite"
    assert data == snapshot


def test_circular_references_error_instead_of_overflowing():
    ctx = CompileContext().with_collection("dragons", [{"id": 1, "dragon_id": 1}])

    with pytest.raises(MaxDepthExceededError):
        DataCompiler().compile({"dragon_id": 1}, ctx)


def test_chest_rewards_without_ids_or_resources_are_tolerated():
    section = chests_section()
    section["rewards"].append({"reward": {}})
    section["rewards"].append("not a dict")
    section["rewards"][0]["reward"] = {"resource": {}}

    chest = ChestsMapper(localization()).map(section)[0]

    assert chest["rewards"][0]["reward"] == {}


def test_maze_nodes_and_paths_with_optional_fields():
    from dc_config_mapper.schemas.maze import MazeNodeIn, MazePathIn

    node = MazeNodeIn.model_validate(
        {"id": 1, "position": [0, 0], "encounter_skip_cost": {"ep": 4}, "key": 2, "encounter": 3}
    ).transform()

    assert node == {
        "id": 1, "cost": 0, "key_path_id": 2, "encounter_id": 3, "encounter_skip_cost": 4,
    }

    path = MazePathIn.model_validate(
        {
            "id": 1, "color": [1], "visibility": 1, "dragon_type": 2, "new_badge": 0, "mobile_dragon_scale": 1,
            "mobile_dragon_offset": [0], "nodes": [], "availability": {"from": 0, "to": 1},
        }
    ).transform()

    assert path["availability"] == {"from": "1970-01-01T00:00:00.000Z", "to": "1970-01-01T00:00:01.000Z"}
    assert path["has_new_badge"] is False


def test_chest_reward_without_resource_keeps_the_other_parts():
    section = chests_section()
    section["rewards"][0]["reward"] = {
        "buildings": [1],
        "skin": [2],
        "moves": 3,
        "seeds": [{"id": 1, "amount": 2}],
        "rarity_seeds": [{"rarity": "C", "amount": 1}],
        "battleground_keys": [{"battleground_id": 1, "key_id": 2, "amount": 3}],
    }

    reward = ChestsMapper(localization()).map(section)[0]["rewards"][0]["reward"]

    assert reward == {
        "building_ids": [1],
        "skin_ids": [2],
        "moves": 3,
        "seeds": [{"id": 1, "amount": 2}],
        "rarity_seeds": [{"rarity": "C", "amount": 1}],
        "battleground_keys": [{"battleground_id": 1, "key_id": 2, "amount": 3}],
    }
