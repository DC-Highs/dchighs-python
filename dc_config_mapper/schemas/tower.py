from typing import Any, List, Optional

from pydantic import Field

from dc_config_mapper.schemas.base import Loose, Strict, dump
from dc_config_mapper.schemas.maze import Ep
from dc_config_mapper.utils import (
    JsonDict,
    Num,
    availability_from_ts,
    basename,
    number_to_boolean,
    process_rewards,
    put,
    size_from_pair,
)


class TowerIslandIn(Strict):
    """Raw tower island (``tower_island.islands[]``) plus the injected ``square_ids``/``floor_ids``/``reward_ids``."""

    id: Num
    analytics_id: str
    tid_name: str
    start_ts: Num
    end_ts: Num
    initial_square_id: Num
    tutorial_id: Num
    tutorial_die_result: Num
    pool_size: Num
    pool_time: Num
    initial_points: Num
    currency_id: Num
    min_level: Num
    building_id: Num
    building_position: List[Num]
    tower_size: List[Num]
    zip_file: str
    sound_tag: str
    canvas_assets_url: str
    mobile_first_floor_position: List[Num]
    mobile_floor_height: Num
    mobile_interior_wall_margin: Num
    mobile_final_dragon_scale: List[Num]
    mobile_final_dragon_position: List[Num]
    mobile_final_dragon_info_position: List[Num]
    max_die_roll: Num
    help_view_id: Num
    active_platforms: Any
    square_ids: List[Num]
    floor_ids: List[Num]
    reward_ids: List[Num]

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "name_key": self.tid_name,
            "availability": availability_from_ts(self.start_ts, self.end_ts),
            "initial_square_id": self.initial_square_id,
            "pool": {"size": self.pool_size, "time": self.pool_time},
            "initial_points": self.initial_points,
            "currency_id": self.currency_id,
            "min_level": self.min_level,
            "zip_file_name": basename(self.zip_file),
            "sound_tag": self.sound_tag,
            "max_die_roll": self.max_die_roll,
            "help_view_id": self.help_view_id,
            "square_ids": self.square_ids,
            "floor_ids": self.floor_ids,
            "reward_ids": self.reward_ids,
            "board_size": size_from_pair(self.tower_size),
        }


class TowerFloorIn(Strict):
    """Raw tower floor (``tower_island.floors[]``)."""

    id: Num
    y: Num
    x_flip: Num
    floor_image: str
    area: Num
    roll_die_price: Ep
    island_id: Num

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "y": self.y,
            "x_flip": number_to_boolean(self.x_flip),
            "floor_image": self.floor_image,
            "area": self.area,
            "roll_die_price": self.roll_die_price.ep,
        }


class TowerRewardEntry(Loose):
    chest: Optional[Num] = None
    egg: Optional[Num] = None


class TowerSquareIn(Strict):
    """Raw tower square (``tower_island.squares[]``)."""

    id: Num
    kind: str = Field(alias="type")
    highlight: Num
    x: Num
    y: Num
    island_id: Num
    ixy: str
    rewards_array: Optional[List[TowerRewardEntry]] = None
    wall: Optional[str] = None
    catapult_destination_square_id: Optional[Num] = None
    piece_reward_id: Optional[Num] = None

    def transform(self) -> JsonDict:
        rewards = None

        if self.rewards_array is not None:
            rewards = process_rewards([dump(entry) for entry in self.rewards_array])

        square: JsonDict = {
            "id": self.id,
            "type": self.kind,
            "is_highlight": number_to_boolean(self.highlight),
            "x": self.x,
            "y": self.y,
            "ixy": self.ixy,
            "rewards": rewards,
        }

        return put(
            square,
            wall=self.wall,
            catapult_destination_square_id=self.catapult_destination_square_id,
            piece_reward_id=self.piece_reward_id,
        )


class TowerRewardIn(Strict):
    """Raw tower reward (``tower_island.rewards[]``)."""

    id: Num
    dragon_reward_id: Num
    last_piece_cost: Num
    num_pieces: Num
    show_new_badge: Num
    area: Num
    island_id: Num

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "dragon_id": self.dragon_reward_id,
            "last_piece_cost": self.last_piece_cost,
            "pieces_count": self.num_pieces,
            "show_new_badge": number_to_boolean(self.show_new_badge),
            "area": self.area,
        }
