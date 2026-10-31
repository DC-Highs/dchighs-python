from typing import List, Optional

from pydantic import Field, StrictBool

from dc_config_mapper.schemas.base import Loose, Strict, dump
from dc_config_mapper.utils import (
    JsonDict,
    Num,
    availability_from_ts,
    basename,
    number_to_boolean,
    process_rewards,
    put,
)

_MISSION_NAME_KEYS = {
    "feed": "tid_runner_mission_feed",
    "gold": "tid_runner_mission_collect_gold",
    "food": "tid_runner_mission_collect_food",
    "breed": "tid_runner_mission_breed",
    "hatch": "tid_runner_mission_hatch",
    "pvp": "tid_runner_mission_pvp",
    "battle": "tid_runner_mission_battle",
}


def runner_island_mission_name_key(mission_type: str) -> Optional[str]:
    """Translation key of each runner mission type."""
    return _MISSION_NAME_KEYS.get(mission_type)


class RunnerIslandIn(Strict):
    """Raw runner island (``runner_island.islands[]``)."""

    id: Num
    start_ts: Num
    end_ts: Num
    building_id: Num
    building_position: List[Num]
    dragon_id: Num
    dragon_offset: List[Num]
    dragon_scale: Num
    runner_dragon_asset: Optional[str] = None
    zip_file: str
    help_id: Num
    run_cost: Num
    sound_tag: str
    mission_pool: List[Num]
    sections: List[Num]
    building_tooltip_position: List[Num]
    building_timer_position: List[Num]
    milestone_rewards: List[Num]

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "availability": availability_from_ts(self.start_ts, self.end_ts),
            "name_key": f"tid_runner_island_{self.id}_title",
            "sound_tag": self.sound_tag,
            "zip_file_name": basename(self.zip_file),
            "run_cost": self.run_cost,
            "mission_pool_ids": self.mission_pool,
            "milestone_reward_ids": self.milestone_rewards,
        }


class RunnerMilestoneRewardIn(Strict):
    """Raw milestone reward (``runner_island.milestone_rewards[]``)."""

    id: Num
    points: Num
    reward_id: Num
    highlighted: Num
    focused: Num

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "points": self.points,
            "reward_id": self.reward_id,
            "is_highlight": number_to_boolean(self.highlighted),
            "is_focused": number_to_boolean(self.focused),
        }


class RunnerMissionIn(Strict):
    """Raw mission (``runner_island.missions[]``)."""

    id: Num
    kind: str = Field(alias="type")
    goal_points: Num
    price: Num
    price_increment: Num
    pool_size: Num
    spawn_time: Num
    collect_chance: Num
    collect_chance_modifier: Num
    energy: Num

    def transform(self) -> JsonDict:
        mission: JsonDict = {"id": self.id, "type": self.kind}

        put(mission, name_key=runner_island_mission_name_key(self.kind))

        mission.update(
            {
                "goal_points": self.goal_points,
                "price": self.price,
                "price_increment": self.price_increment,
                "pool_size": self.pool_size,
                "spawn_time": self.spawn_time,
                "collect_chance": self.collect_chance,
                "collect_chance_modifier": self.collect_chance_modifier,
                "points": self.energy,
            }
        )

        return mission


class RunnerMissionPoolIn(Strict):
    """Raw mission pool (``runner_island.mission_pool[]``)."""

    id: Num
    buy_all_discounts: Num
    missions: List[Num]
    price: Num
    price_increment: Num

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "buy_all_discounts": self.buy_all_discounts,
            "mission_ids": self.missions,
            "price": self.price,
            "price_increment": self.price_increment,
        }


class RunnerSeed(Loose):
    id: Num
    amount: Num


class RunnerRewardEntry(Loose):
    """One entry of ``reward[]``. Field order is the order :func:`process_rewards` expects."""

    chest: Optional[Num] = None
    ep: Optional[Num] = None
    egg: Optional[Num] = None
    c: Optional[Num] = None
    seeds: Optional[List[RunnerSeed]] = None
    f: Optional[Num] = None
    g: Optional[Num] = None
    en_runner: Optional[Num] = None
    f_token: Optional[Num] = None
    pu_token: Optional[Num] = None
    i_token: Optional[Num] = None
    wr_token: Optional[Num] = None
    el_token: Optional[Num] = None
    wd_token: Optional[Num] = None
    m_token: Optional[Num] = None
    w_token: Optional[Num] = None
    pr_token: Optional[Num] = None
    e_token: Optional[Num] = None
    d_token: Optional[Num] = None
    p_token: Optional[Num] = None
    li_token: Optional[Num] = None
    l_token: Optional[Num] = None


class RunnerRewardIn(Strict):
    """Raw runner reward (``runner_island.rewards[]``)."""

    id: Num
    reward: List[RunnerRewardEntry]
    type_id: Num
    double_with_video_ad: Optional[StrictBool] = None
    premium_rewards: Optional[List[Num]] = None
    new_badge: Optional[List[Num]] = None

    def transform(self) -> JsonDict:
        reward: JsonDict = {
            "id": self.id,
            "rewards": process_rewards([dump(entry) for entry in self.reward]),
            "type_id": self.type_id,
        }

        return put(
            reward,
            double_with_video_ad=self.double_with_video_ad,
            premium_rewards=self.premium_rewards,
            new_badge=self.new_badge,
        )
