from typing import Any, List, Optional, Union

from pydantic import Field, StrictBool

from dc_config_mapper.schemas.base import Loose, Strict, dump
from dc_config_mapper.utils import (
    JsonDict,
    Num,
    availability_from_ts,
    basename,
    iso_from_ts,
    number_to_boolean,
    process_rewards,
    put,
)


class TsRange(Loose):
    from_: Num = Field(alias="from")
    to: Num


class Ep(Loose):
    ep: Num


class MazeIslandIn(Strict):
    """Raw maze island (``maze_island.islands[]``)."""

    id: Num
    tid_name: str
    name: str
    availability: TsRange
    paths: List[Num]
    happy_hours: List[Any]
    currency_id: Num
    pool_size: Num
    pool_time: Num
    initial_points: Num
    clouds: List[Any]
    cloud_radius: Num
    dragon_radius: Num
    min_level: Num
    building_id: Num
    mobile_tutorial_id: Num
    tutorial_path_id: Num
    tutorial_initial_camera_position: List[Num]
    tutorial_initial_zoom: Num
    tutorial_final_zoom: Num
    zip_file: str
    mobile_building_position: List[Num]
    active_platforms: Any
    help_view_id: Num
    sound_tag: str

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "name": self.name,
            "name_key": self.tid_name,
            "availability": availability_from_ts(self.availability.from_, self.availability.to),
            "path_ids": self.paths,
            "currency_id": self.currency_id,
            "pool": {"size": self.pool_size, "time": self.pool_time},
            "initial_points": self.initial_points,
            "min_level": self.min_level,
            "zip_file_name": basename(self.zip_file),
            "sound_tag": self.sound_tag,
        }


class MazeRewardEntry(Loose):
    chest: Optional[Num] = None
    b: Optional[Union[Num, List[Num]]] = None
    f: Optional[Num] = None
    g: Optional[Num] = None


class MazeNodeIn(Strict):
    """Raw maze node (``maze_island.nodes[]``)."""

    id: Num
    position: List[Num]
    cost: Optional[Ep] = None
    reward_id: Optional[Num] = None
    reward: Optional[List[MazeRewardEntry]] = None
    highlighted: Optional[StrictBool] = None
    key: Optional[Num] = None
    encounter: Optional[Num] = None
    encounter_skip_cost: Optional[Ep] = None

    def transform(self) -> JsonDict:
        rewards = None

        if self.reward is not None:
            rewards = process_rewards([dump(entry) for entry in self.reward])

        node: JsonDict = {"id": self.id, "cost": self.cost.ep if self.cost is not None else 0}

        put(
            node,
            rewards=rewards,
            is_highlighted=self.highlighted,
            key_path_id=self.key,
            encounter_id=self.encounter,
        )

        node["encounter_skip_cost"] = self.encounter_skip_cost.ep if self.encounter_skip_cost is not None else None
        return node


class MazePathIn(Strict):
    """Raw maze path (``maze_island.paths[]``)."""

    id: Num
    color: List[Num]
    visibility: Num
    dragon_type: Num
    new_badge: Num
    mobile_dragon_scale: Num
    mobile_dragon_offset: List[Num]
    nodes: List[Num]
    availability: Optional[TsRange] = None

    def transform(self) -> JsonDict:
        path: JsonDict = {
            "id": self.id,
            "color": self.color,
            "visibility": self.visibility,
            "dragon_id": self.dragon_type,
            "has_new_badge": number_to_boolean(self.new_badge),
            "node_ids": self.nodes,
        }

        if self.availability is not None:
            path["availability"] = {
                "from": iso_from_ts(self.availability.from_),
                "to": iso_from_ts(self.availability.to),
            }

        return path
