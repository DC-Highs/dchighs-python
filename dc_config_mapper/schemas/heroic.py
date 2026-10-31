from typing import Any, List, Optional

from pydantic import Field, field_validator

from dc_config_mapper.schemas.base import Loose, Strict, coerce_number_list, dump
from dc_config_mapper.utils import (
    JsonDict,
    Num,
    basename,
    iso_from_ts,
    num_mul,
    num_sub,
    number_to_boolean,
    process_rewards,
)


class HeroicRacesIslandIn(Strict):
    """Raw heroic race (``heroic_races.islands[]``)."""

    id: Num
    active_platforms: Any
    min_level: Num
    start_ts: Num
    end_ts: Num
    end_ts_threshold: Num
    secs_before_cache_freeze: Num
    min_qualifying_laps: Num
    laps: List[Num]
    building_id: Num
    building_id_96: Num
    building_claim_id: Num
    building_free_spin_id: Num
    building_position: List[Num]
    dragon_building_position: List[Num]
    dragon_building_scale: Num
    zip_file: str
    canvas_assets_url: str
    island_title_tid: str
    sound_tag: str
    level_tiers: List[Num]
    rewards: List[Num]
    dragon_race_id: Num
    dragon_race_scale: Num
    dragon_race_offset: List[Num]
    dragon_reward_scale: Num
    dragon_reward_offset: List[Num]
    help_id: Num
    dragon_is_new: Num
    spinner_enabled: Num
    spin_rewards: List[Num]
    spin_cooldown: Num
    buy_spin_price: Num
    notification_anim_remaining_time: Num
    notification_anim_per_day: Num
    notification_anim_duration: Num
    lap_completed_to_hide_notification: Num

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "min_level": self.min_level,
            "availability": {
                "from": iso_from_ts(self.start_ts),
                "to": iso_from_ts(self.end_ts),
                "to_threshold": self.end_ts_threshold,
            },
            "name_key": self.island_title_tid,
            "sound_tag": self.sound_tag,
            "zip_file_name": basename(self.zip_file),
            "min_qualifying_laps": self.min_qualifying_laps,
            "lap_ids": self.laps,
            "level_tier_ids": self.level_tiers,
            "reward_ids": self.rewards,
            "race": {
                "dragon_id": self.dragon_race_id,
                "dragon_is_new": number_to_boolean(self.dragon_is_new),
            },
            "spinner_enabled": self.spinner_enabled,
            "spin_cooldown": self.spin_cooldown,
            "spin_rewards": self.spin_rewards,
            "buy_spin_price": self.buy_spin_price,
        }


class HeroicRewardEntry(Loose):
    egg: Optional[List[Num]] = None
    c: Optional[Num] = None


class HeroicRewardIn(Strict):
    """Raw heroic race reward (``heroic_races.rewards[]``)."""

    id: Num
    positions: List[Num]
    rewards: List[HeroicRewardEntry]

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "positions": self.positions,
            "reward": process_rewards([dump(entry) for entry in self.rewards]),
        }


class HeroicEncounterIn(Strict):
    """Raw encounter (``heroic_races.encounters[]``)."""

    id: Num
    enemies: List[Num]
    speed_up_price_per_hour: Num
    fight_background_id: str

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "enemy_ids": self.enemies,
            "speed_up_price_per_hour": self.speed_up_price_per_hour,
            "fight_background_id": self.fight_background_id,
        }


class HeroicEnemy(Strict):
    """Enemy (``heroic_races.enemies[]``): validated and returned unchanged, except that
    ``dragon_ids``/``enemies`` are coerced to numbers (they come as strings sometimes)."""

    id: Num
    dragon_ids: List[Num]
    handicaps: List[Num]
    view_type: str
    elements_view_type: List[Any]
    cooldown: Num
    enemies: Optional[List[Num]] = None

    @field_validator("dragon_ids", "enemies", mode="before")
    @classmethod
    def _coerce(cls, value: Any) -> Any:
        return coerce_number_list(value)

    def transform(self) -> JsonDict:
        enemy = self.model_dump()

        if enemy["enemies"] is None:
            del enemy["enemies"]

        return enemy


class HeroicLapIn(Strict):
    """Raw lap (``heroic_races.laps[]``)."""

    id: Num
    nodes: List[Num]

    def transform(self) -> JsonDict:
        return {"id": self.id, "node_ids": self.nodes}


class HeroicMissionIn(Strict):
    """Raw mission (``heroic_races.missions[]``)."""

    id: Num
    kind: str = Field(alias="type")
    goal_points: Num
    price: Num
    price_increment: Num
    pool_size: Num
    spawn_time: Num
    collect_chance: Num
    collect_chance_modifier: Num
    encounter: Optional[Num] = None

    def transform(self) -> JsonDict:
        mission: JsonDict = {
            "id": self.id,
            "type": self.kind,
            "goal_points": self.goal_points,
            "price": self.price,
            "price_increment": self.price_increment,
            "pool_size": self.pool_size,
            "spawn_time": {
                "one": self.spawn_time,
                "all": num_mul(self.spawn_time, num_sub(self.goal_points, self.pool_size)),
            },
            "collect_chance": self.collect_chance,
            "collect_chance_modifier": self.collect_chance_modifier,
        }

        if self.encounter is not None:
            mission["encounter_id"] = self.encounter

        return mission


class HeroicNodeIn(Strict):
    """Raw node (``heroic_races.nodes[]``)."""

    id: Num
    buy_all_discount: Num
    missions: List[Num]

    def transform(self) -> JsonDict:
        return {"id": self.id, "buy_all_discount": self.buy_all_discount, "mission_ids": self.missions}
