import pytest

from dc_config_mapper import (
    FogIslandsMapper,
    GridIslandsMapper,
    HeroicRacesMapper,
    ItemsMapper,
    MissingFieldError,
    RunnerIslandsMapper,
    SchemaError,
    SkillsMapper,
    TowerIslandsMapper,
)
from dc_config_mapper.mappers import MappedResult, Mapper
from dc_core import ConfigLanguage
from dc_localization import Localization
from sample_sections import (
    building_item,
    clone,
    dragon_item,
    fog_section,
    grid_section,
    heroic_section,
    runner_section,
    skills_section,
    tower_section,
)


def localization() -> Localization:
    return Localization(
        ConfigLanguage.ENGLISH,
        {
            "tid_fog": "Fog",
            "tid_grid": "Grid",
            "tid_episode": "Episode",
            "tid_tower": "Tower",
            "tid_heroic": "Heroic",
            "tid_runner_island_5_title": "Runner",
            "tid_bite": "Bite!",
            "tid_runner_mission_feed": "Feed",
            "tid_unit_1000_name": "Nature Dragon",
            "tid_unit_1000_description": "Green",
        },
    )


def test_fog_islands():
    fog = FogIslandsMapper(localization()).map(fog_section())

    assert fog.islands[0]["name"] == "Fog"
    assert fog.islands[0]["square_ids"] == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert fog.islands[0]["board_size"] == {"width": 10, "height": 20}
    assert fog.islands[0]["cell_size"] == {"width": 5}
    assert fog.islands[0]["zip_file_name"] == "fog.zip"

    rewards = {square["id"]: square["reward"] for square in fog.squares}
    assert rewards[1] == {"type": "CHEST", "chest_id": 9}
    assert rewards[2] == {"type": "CHEST"}
    assert rewards[3] == {"type": "RESOURCE", "skin_id": 77}
    assert rewards[4] == {"type": "RESOURCE"} and rewards[5] == {"type": "RESOURCE"}
    assert rewards[6] is None and rewards[7] is None
    assert rewards[8] == {"type": "PIECE", "piece_dragon_id": 1042}
    assert rewards[9] == {"type": "PIECE"}
    assert fog.squares[0]["reward_id"] == 4 and "reward_id" not in fog.squares[1]
    assert fog.rewards[0] == {
        "id": 1, "type": "DRAGON", "dragon_id": 1042, "last_piece_cost": 5, "num_pieces": 3, "show_new_badge": False,
    }
    assert fog.to_dict()["hints"] == [3]


def test_grid_islands():
    grid = GridIslandsMapper(localization()).map(grid_section())

    assert grid.islands[0]["name"] == "Grid"
    assert grid.islands[0]["episode_ids"] == [1]
    assert grid.islands[0]["board_size"] == {"width": 4, "height": 4}
    assert grid.episodes[0]["name"] == "Episode"
    assert grid.episodes[0]["decoration_ids"] == [1]
    assert [square["reward"] for square in grid.squares] == [
        None,
        {"type": "chest", "chest_id": 5},
        {"type": "dragon", "dragon_id": 1042},
        {"type": "dragon"},
    ]
    assert grid.squares[1]["wall"] == "w" and grid.squares[1]["resource"] == {"a": 1}
    assert "wall" not in grid.squares[0]
    assert grid.decorations[0] == {"id": 1, "file_name": "deco.png", "x": 1, "y": 2}
    assert grid.encounters[0]["enemy_ids"] == [1, 2]
    assert grid.enemies == [1] and grid.currencies == [2] and grid.actions == [3] and grid.parameters == [4]


def test_tower_islands():
    tower = TowerIslandsMapper(localization()).map(tower_section())

    island = tower.islands[0]
    assert island["name"] == "Tower"
    assert (island["square_ids"], island["floor_ids"], island["reward_ids"]) == ([1, 2], [1], [1])
    assert island["board_size"] == {"width": 3, "height": 4}
    assert tower.floors[0]["x_flip"] is True and tower.floors[0]["roll_die_price"] == 3
    assert tower.squares[0]["rewards"] == [
        {"type": "chest", "chest_id": 5},
        {"type": "dragon", "dragon_id": 1042},
    ]
    assert tower.squares[0]["wall"] == "w" and tower.squares[0]["piece_reward_id"] == 3
    assert tower.squares[1]["rewards"] is None and "wall" not in tower.squares[1]
    assert tower.rewards[0]["pieces_count"] == 3
    assert tower.happy_hours == [{"name_key": "tid_x"}]


def test_runner_islands():
    runner = RunnerIslandsMapper(localization()).map(runner_section())

    assert runner.islands[0]["name"] == "Runner"
    assert runner.islands[0]["mission_pool_ids"] == [1]
    assert runner.missions[0]["name"] == "Feed"
    assert "name_key" not in runner.missions[1] and runner.missions[1]["points"] == 4
    assert runner.rewards[0]["rewards"][0] == {"type": "gold", "amount": 10}
    assert runner.rewards[0]["double_with_video_ad"] is True
    assert runner.rewards[0]["premium_rewards"] == [1] and runner.rewards[0]["new_badge"] == [2]
    assert "double_with_video_ad" not in runner.rewards[1]
    assert runner.milestone_rewards[0]["is_highlight"] is True and runner.milestone_rewards[0]["is_focused"] is False
    assert runner.mission_pools[0]["mission_ids"] == [1, 2]
    assert runner.to_dict()["milestones"] == [8]


def test_skills():
    skills = SkillsMapper(localization()).map(skills_section())

    assert skills.attacks[0]["name"] == "Bite!"
    assert skills.attacks[0]["element"] == "flame"
    assert skills.attacks[0]["effect_atk"] == "e" and skills.attacks[0]["skill_id"] == 4
    assert "element" not in skills.attacks[1] and "skill_id" not in skills.attacks[1]
    assert skills.to_dict()["world_skills"] == []


def test_heroic_races():
    heroic = HeroicRacesMapper(localization()).map(heroic_section())

    island = heroic.islands[0]
    assert island["name"] == "Heroic"
    assert island["availability"] == {
        "from": "1970-01-01T00:00:00.000Z", "to": "2023-11-14T22:13:20.000Z", "to_threshold": 3,
    }
    assert island["race"] == {"dragon_id": 1042, "dragon_is_new": True}
    assert heroic.rewards[0]["reward"] == [
        {"type": "dragon", "dragon_ids": [1042]},
        {"type": "gem", "amount": 5},
    ]
    assert heroic.encounters[0]["fight_background_id"] == "f"
    assert heroic.enemies[0]["dragon_ids"] == [1, 2.5] and "enemies" not in heroic.enemies[0]
    assert heroic.enemies[1]["dragon_ids"] == [1, 0, 0, 100.0] and heroic.enemies[1]["enemies"] == [4]
    assert heroic.laps[0] == {"id": 1, "node_ids": [1]}
    assert heroic.missions[0]["spawn_time"] == {"one": 1.5, "all": 9}
    assert heroic.missions[0]["encounter_id"] == 3
    assert heroic.nodes[0]["mission_ids"] == [1]
    assert heroic.lap_rewards == [1] and heroic.nodes_position == [2] and heroic.spin_rewards == [4]


@pytest.mark.parametrize("bad", ["abc", {"a": 1}, [1]])
def test_heroic_enemy_rejects_uncoercible_numbers(bad):
    section = heroic_section()
    section["enemies"][0]["dragon_ids"] = [bad]

    with pytest.raises(SchemaError):
        HeroicRacesMapper(localization()).map(section)


def test_heroic_enemy_requires_a_list():
    section = heroic_section()
    section["enemies"][0]["dragon_ids"] = "1"

    with pytest.raises(SchemaError):
        HeroicRacesMapper(localization()).map(section)


def test_items_dragons_and_buildings():
    items = ItemsMapper(localization()).map([dragon_item(), building_item(), {"id": 5}, {"group_type": 5}])

    dragon = items.dragons[0]
    assert dragon["name"] == "Nature Dragon" and dragon["description"] == "Green"
    assert dragon["elements"] == ["flame", None]
    assert dragon["buy_price"] == {"type": "gold", "amount": 100}
    assert dragon["sell_price"] == {"type": "gold", "amount": 10}
    assert (dragon["is_breedable"], dragon["can_breed"], dragon["is_in_store"]) == (False, True, True)
    assert dragon["passive_skill_ids"] is None and dragon["tags"] == []
    assert dragon["image_names"] == {"default": None, "mobile": None, "android": None}
    assert dragon["stats"] == {"attack": 1, "life": 1, "speed": 1, "level": 1}
    assert dragon["timers"]["hatching"] == {"default": 60}

    building = items.buildings[0]
    assert building["buy_price"] == {"type": "gem", "amount": 5}
    assert building["sell_price"] is None
    assert building["properties"] == {"capacity": 3, "workingBuilding": 1, "fixed_position": [1, 2]}
    assert building["imageNames"] == {"default": "i", "mobile": "m", "android": "a"}
    assert building["animated"] is True and building["new_item"] is False
    assert "name_key" not in building and "inventory_ids" not in building
    assert set(items.group_keys()) >= {"dragons", "buildings", "habitats"}
    assert items["dragons"] is items.dragons and "dragons" in items and "nope" not in items
    assert items.to_dict()["buildings"] == items.buildings


def test_items_optional_fields():
    full_dragon = dragon_item(
        description="D", tags=["a"], speed_override=3, passive_skills=[1], post_skills=[2],
        img_name="i", img_name_mobile="m", img_name_android="a", giftable=1, in_store_ch=1,
        costs_ch_1={"c": 1}, costs_ch_2={"g": 2}, hatching_time_reawaken=1, breeding_time_reawaken=2,
        hatching_time_ngu_aggressive=3, breeding_time_ngu_aggressive=4, hatching_time_ngu_soft=5,
        breeding_time_ngu_soft=6, costs={"c": 1},
    )
    full_building = building_item(
        name_key="tid_b", element_type="fire", cost_unit_cash=1, collect_xp=2, collect_type={"a": 1},
        description="B", sell_price={"g": 4}, inventory_ids=7,
    )

    items = ItemsMapper(localization()).map([full_dragon, full_building])
    dragon, building = items.dragons[0], items.buildings[0]

    assert dragon["description"] == "Green" and dragon["tags"] == ["a"]
    assert dragon["stats"]["speed_override"] == 3
    assert dragon["passive_skill_ids"] == [1] and dragon["post_skill_ids"] == [2]
    assert dragon["buy_price"] == {"type": "gem", "amount": 1}
    assert dragon["timers"]["hatching"] == {
        "default": 60, "hatching_reawaken": 1, "hatching_ngu_aggressive": 3, "hatching_ngu_soft": 5,
    }
    assert dragon["timers"]["breeding"]["breeding_ngu_soft"] == 6
    assert dragon["image_names"] == {"default": "i", "mobile": "m", "android": "a"}
    assert building["name_key"] == "tid_b" and building["name"] == "Hatchery"
    assert building["sell_price"] == {"type": "gold", "amount": 4}
    assert building["collect_type"] == {"a": 1} and building["inventory_ids"] == 7
    assert building["cost_unit_cash"] == 1 and building["collect_xp"] == 2 and building["description"] == "B"
    assert building["element_type"] == "fire"


def test_items_errors():
    with pytest.raises(MissingFieldError):
        ItemsMapper(localization()).map({"not": "a list"})

    broken = clone(building_item())
    del broken["width"]

    with pytest.raises(SchemaError) as error:
        ItemsMapper(localization()).map([broken])

    assert error.value.schema == "building"


def test_missing_arrays_are_reported():
    section = fog_section()
    del section["squares"]

    with pytest.raises(MissingFieldError) as error:
        FogIslandsMapper(localization()).map(section)

    assert error.value.key == "squares"
    assert "squares" in str(error.value)


def test_mapper_base_classes():
    mapper = Mapper(localization())

    assert mapper.translate_all({"list": [{"name_key": "tid_fog"}, 3]}, "list") == [{"name": "Fog"}, 3]
    assert mapper.translated({"tid_name": "tid_fog"}) == {"name": "Fog"}
    assert issubclass(type(FogIslandsMapper(localization())), Mapper)
    assert MappedResult.to_dict.__doc__
