"""Minimal but schema-valid configuration sections used by the mapper tests."""

import copy


def fog_section():
    island = {
        "id": 1, "analytics_id": "a", "tid_name": "tid_fog", "tutorial_id": 1, "tutorial_claimable_cell_id": 1,
        "board_size": [10, 20], "cell_size": [5], "origin_offset": [0, 0], "initial_square_id": 1,
        "pool_points": 5, "pool_time": 60, "initial_points": 3, "start_ts": 0, "end_ts": 1700000000,
        "currency_id": 1, "min_level": 7, "building_id": 1, "building_position": [0, 0],
        "zip_file": "x/y/fog.zip", "sound_tag": "FOG", "canvas_assets_url": "u", "background_plist": "p",
        "foregrounds_plists": [], "particles_position": [0, 0], "tutorial_claim_cells": [1],
    }

    def square(square_id, kind, **extra):
        base = {
            "id": square_id, "type": kind, "highlight": 1, "x": 1, "y": 2, "island_id": 1,
            "claim_cost": 10, "come_back_cost": 5,
        }
        base.update(extra)
        return base

    return {
        "islands": [island, dict(island, id=2)],
        "squares": [
            square(1, "CHEST", type_id=9, reward_id=4),
            square(2, "CHEST"),
            square(3, "RESOURCE", resource={"skin": 77}),
            square(4, "RESOURCE", resource={}),
            square(5, "RESOURCE"),
            square(6, "NONE"),
            square(7, "STEP"),
            square(8, "PIECE", type_id=1042),
            square(9, "PIECE"),
        ],
        "rewards": [
            {"id": 1, "type": "DRAGON", "island_id": 1, "reward_id": 1042, "last_piece_cost": 5,
             "num_pieces": 3, "show_new_badge": 0}
        ],
        "currencies": [1],
        "actions": [2],
        "hints": [3],
        "parameters": [4],
    }


def grid_section():
    island = {
        "id": 1, "analytics_id": "a", "tid_name": "tid_grid", "tutorial_id": 1, "tutorial_claimable_cell_id": 1,
        "pool_points": 5, "pool_time": 60, "initial_points": 3, "start_ts": 0, "end_ts": 1700000000,
        "currency_id": 1, "min_level": 7, "building_id": 1, "building_position": [0, 0], "zip_file": "g.zip",
        "sound_tag": "GRID", "canvas_assets_url": "u", "ui_configuration": {}, "active_platforms": [],
        "episodes": [1], "board_size": [4, 4], "initial_square_id": 1, "backgrounds": [1],
        "background_plist": "p", "foregrounds": [], "foregrounds_plists": [],
    }
    episode = {
        "id": 1, "island_id": 1, "board_size": [4, 4], "initial_square_id": 1, "final_square_id": 2,
        "tid_title": "tid_episode", "mobile_begin_tutorial_id": 1, "mobile_end_tutorial_id": 2,
        "canvas_background": "c", "backgrounds": ["b"], "background_plist": "p", "foregrounds": [],
        "foregrounds_plists": [], "squares": [1, 2, 3, 4],
    }

    def square(square_id, kind, **extra):
        base = {
            "id": square_id, "type": kind, "highlight": 0, "x": 1, "y": 1, "island_id": 1, "episode_id": 1,
            "claim_cost": 3,
        }
        base.update(extra)
        return base

    return {
        "islands": [island],
        "episodes": [episode],
        "squares": [
            square(1, "NONE"),
            square(2, "CHEST", type_id=5, wall="w", wall_suffix="s", resource={"a": 1}),
            square(3, "DRAGON", type_id=1042),
            square(4, "DRAGON"),
        ],
        "decorations": [
            {"id": 1, "file": "deco", "x": 1, "y": 2, "island_id": 1, "episode_id": 1},
            {"id": 2, "file": "deco2", "x": 3, "y": 4, "island_id": 1, "episode_id": 2},
        ],
        "encounters": [
            {"id": 1, "enemies": [1, 2], "speed_up_price_per_hour": 5, "fight_background": "f",
             "fight_background_id": "fi"}
        ],
        "enemies": [1],
        "currencies": [2],
        "actions": [3],
        "parameters": [4],
    }


def tower_section():
    island = {
        "id": 1, "analytics_id": "a", "tid_name": "tid_tower", "start_ts": 0, "end_ts": 1700000000,
        "initial_square_id": 1, "tutorial_id": 1, "tutorial_die_result": 1, "pool_size": 5, "pool_time": 60,
        "initial_points": 3, "currency_id": 1, "min_level": 7, "building_id": 1, "building_position": [0, 0],
        "tower_size": [3, 4], "zip_file": "t.zip", "sound_tag": "T", "canvas_assets_url": "u",
        "mobile_first_floor_position": [0, 0], "mobile_floor_height": 1, "mobile_interior_wall_margin": 1,
        "mobile_final_dragon_scale": [1], "mobile_final_dragon_position": [1], "mobile_final_dragon_info_position": [1],
        "max_die_roll": 6, "help_view_id": 1, "active_platforms": {},
    }
    return {
        "islands": [island],
        "floors": [
            {"id": 1, "y": 5, "x_flip": 1, "floor_image": "f", "area": 1, "roll_die_price": {"ep": 3}, "island_id": 1}
        ],
        "squares": [
            {"id": 1, "type": "A", "highlight": 0, "x": 1, "y": 1, "island_id": 1, "ixy": "1_1",
             "rewards_array": [{"chest": 5}, {"egg": 1042}], "wall": "w", "catapult_destination_square_id": 2,
             "piece_reward_id": 3},
            {"id": 2, "type": "B", "highlight": 1, "x": 2, "y": 2, "island_id": 1, "ixy": "2_2"},
        ],
        "rewards": [
            {"id": 1, "dragon_reward_id": 1042, "last_piece_cost": 5, "num_pieces": 3, "show_new_badge": 1,
             "area": 1, "island_id": 1}
        ],
        "happy_hours": [{"name_key": "tid_x"}],
        "parameters": [],
        "currencies": [],
        "actions": [],
    }


def runner_section():
    island = {
        "id": 5, "start_ts": 0, "end_ts": 1700000000, "building_id": 1, "building_position": [0, 0],
        "dragon_id": 1, "dragon_offset": [0], "dragon_scale": 1, "runner_dragon_asset": "a", "zip_file": "r.zip",
        "help_id": 1, "run_cost": 10, "sound_tag": "R", "mission_pool": [1], "sections": [1],
        "building_tooltip_position": [0], "building_timer_position": [0], "milestone_rewards": [1],
    }

    def mission(mission_id, kind):
        return {
            "id": mission_id, "type": kind, "goal_points": 1, "price": 1, "price_increment": 1, "pool_size": 1,
            "spawn_time": 1, "collect_chance": 1, "collect_chance_modifier": 1, "energy": 4,
        }

    return {
        "islands": [island],
        "missions": [mission(1, "feed"), mission(2, "unknown")],
        "rewards": [
            {"id": 1, "reward": [{"g": 10}, {"seeds": [{"id": 1, "amount": 2}]}], "type_id": 1,
             "double_with_video_ad": True, "premium_rewards": [1], "new_badge": [2]},
            {"id": 2, "reward": [{"chest": 1}], "type_id": 2},
        ],
        "milestone_rewards": [{"id": 1, "points": 5, "reward_id": 1, "highlighted": 1, "focused": 0}],
        "mission_pool": [{"id": 1, "buy_all_discounts": 1, "missions": [1, 2], "price": 5, "price_increment": 1}],
        "sections": [1],
        "parameters": [2],
        "obstacles": [3],
        "level_chunks": [4],
        "level_rewards": [5],
        "rewards_config": [6],
        "rewards_tiers": [7],
        "milestones": [8],
    }


def skills_section():
    def attack(attack_id, element, **extra):
        base = {
            "id": attack_id, "name": "Bite", "name_key": "tid_bite", "type": "ATTACK", "element": element,
            "damage": 1, "ui_damage": 2, "effect_def": "d", "effect_sfx": 1, "training_time": 1,
            "button_style": 1, "special_icon": 1,
        }
        base.update(extra)
        return base

    return {
        "attacks": [attack(1, "f", effect_atk="e", skill_id=4), attack(2, "zzz")],
        "skills": [{"name_key": "tid_x"}],
        "auras": [],
        "post": [],
        "effects": [],
        "passive": [],
        "world_skills": [],
        "world_effects": [],
        "level_based_parameters": [],
    }


def heroic_section():
    island = {
        "id": 1, "active_platforms": {}, "min_level": 7, "start_ts": 0, "end_ts": 1700000000,
        "end_ts_threshold": 3, "secs_before_cache_freeze": 1, "min_qualifying_laps": 2, "laps": [1],
        "building_id": 1, "building_id_96": 1, "building_claim_id": 1, "building_free_spin_id": 1,
        "building_position": [0], "dragon_building_position": [0], "dragon_building_scale": 1, "zip_file": "h.zip",
        "canvas_assets_url": "u", "island_title_tid": "tid_heroic", "sound_tag": "H", "level_tiers": [1],
        "rewards": [1], "dragon_race_id": 1042, "dragon_race_scale": 1, "dragon_race_offset": [0],
        "dragon_reward_scale": 1, "dragon_reward_offset": [0], "help_id": 1, "dragon_is_new": 1,
        "spinner_enabled": 1, "spin_rewards": [1], "spin_cooldown": 1, "buy_spin_price": 1,
        "notification_anim_remaining_time": 1, "notification_anim_per_day": 1, "notification_anim_duration": 1,
        "lap_completed_to_hide_notification": 1,
    }
    return {
        "islands": [island],
        "rewards": [{"id": 1, "positions": [1, 2], "rewards": [{"egg": [1042]}, {"c": 5}]}],
        "encounters": [{"id": 1, "enemies": [1], "speed_up_price_per_hour": 2, "fight_background_id": "f"}],
        "enemies": [
            {"id": 1, "dragon_ids": ["1", 2.5], "handicaps": [], "view_type": "v", "elements_view_type": [],
             "cooldown": 1},
            {"id": 2, "dragon_ids": [True, None, "  ", "1e2"], "handicaps": [], "view_type": "v",
             "elements_view_type": [], "cooldown": 1, "enemies": [" 4 "]},
        ],
        "laps": [{"id": 1, "nodes": [1]}],
        "missions": [
            {"id": 1, "type": "BREED", "goal_points": 10, "price": 1, "price_increment": 0, "pool_size": 4,
             "spawn_time": 1.5, "collect_chance": 1, "collect_chance_modifier": 0, "encounter": 3},
        ],
        "nodes": [{"id": 1, "buy_all_discount": 2, "missions": [1]}],
        "lap_rewards": [1],
        "nodes_position": [2],
        "parameters": [3],
        "spin_rewards": [4],
    }


def dragon_item(**extra):
    base = {
        "id": 1000, "name": "Dragon", "group_type": "DRAGON", "speed": 1, "mobile_version": 1,
        "android_version": 1, "display_order": 1, "hatching_time": 60, "breeding_time": 120, "xp": 5, "lvl": 1,
        "costs": {"g": 100}, "sell_price": {"g": 10}, "starting_coins": 1, "coins_added": 2, "can_breed": 1,
        "breedable": 0, "deity_breeding": 0, "difficulty": 1, "category": 1, "rarity": 1, "dragon_rarity": "C",
        "attacks": [1], "attributes": ["f", "zzz"], "trainable_attacks": [2], "upgrade_levels": [1],
        "background_vfx": [], "foreground_vfx": [], "in_store": 1, "in_store_min_level": 3, "flying_level": 0,
        "swim": 0, "new_item": 0, "gift_level": 0, "seeds_to_summon": 1, "hatching_time_10": 1,
        "breeding_time_40": 1, "breeding_time_10": 1, "hatching_time_40": 1, "base_attack": 1, "base_life": 1,
        "dragon_ownership_id": 1,
    }
    base.update(extra)
    return base


def building_item(**extra):
    base = {
        "id": 10, "name": "Hatchery", "group_type": "BUILDING", "animated": 1, "build_time": 10,
        "mobile_version": 1, "android_version": 1, "show_on_mobile": 1, "type": "hatchery", "xp": 1,
        "min_level": 1, "costs": {"c": 5}, "display_order": 1, "boost_modifier": 0, "gift_level": 0,
        "giftable": 0, "collect": 0, "category_id": 1, "subcategory_id": 1, "building_limit_same_id": 1,
        "in_store": 1, "width": 2, "height": 2, "new_item": 0, "img_name": "i", "img_name_mobile": "m",
        "img_name_android": "a", "activation": 0, "upgrades_to": 0, "velocity": 0,
        "properties": {"capacity": 3, "workingBuilding": 1, "fixed_position": [1, 2], "unknown": 1},
        "building_ownership_id": 1,
    }
    base.update(extra)
    return base


def clone(value):
    return copy.deepcopy(value)
