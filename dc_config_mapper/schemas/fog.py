from typing import Any, List, Optional

from pydantic import Field

from dc_config_mapper.schemas.base import Strict
from dc_config_mapper.utils import (
    JsonDict,
    Num,
    availability_from_ts,
    basename,
    number_to_boolean,
    put,
    size_from_pair,
)


class FogIslandIn(Strict):
    """Raw fog island (``fog_island.islands[]``) plus the injected ``square_ids``."""

    id: Num
    analytics_id: str
    tid_name: str
    tutorial_id: Num
    tutorial_claimable_cell_id: Num
    board_size: List[Num]
    cell_size: List[Num]
    origin_offset: List[Num]
    initial_square_id: Num
    pool_points: Num
    pool_time: Num
    initial_points: Num
    start_ts: Num
    end_ts: Num
    currency_id: Num
    min_level: Num
    building_id: Num
    building_position: List[Num]
    zip_file: str
    sound_tag: str
    canvas_assets_url: str
    background_plist: str
    foregrounds_plists: List[Any]
    particles_position: List[Num]
    tutorial_claim_cells: List[Num]
    square_ids: List[Num]

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "availability": availability_from_ts(self.start_ts, self.end_ts),
            "name_key": self.tid_name,
            "board_size": size_from_pair(self.board_size),
            "cell_size": size_from_pair(self.cell_size),
            "initial_square_id": self.initial_square_id,
            "pool": {"points": self.pool_points, "time": self.pool_time},
            "initial_points": self.initial_points,
            "currency_id": self.currency_id,
            "min_level": self.min_level,
            "zip_file_name": basename(self.zip_file),
            "sound_tag": self.sound_tag,
            "square_ids": self.square_ids,
        }


class FogRewardIn(Strict):
    """Raw fog island reward (``fog_island.rewards[]``)."""

    id: Num
    kind: str = Field(alias="type")
    island_id: Num
    reward_id: Num
    last_piece_cost: Num
    num_pieces: Num
    show_new_badge: Num

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "type": self.kind,
            "dragon_id": self.reward_id,
            "last_piece_cost": self.last_piece_cost,
            "num_pieces": self.num_pieces,
            "show_new_badge": number_to_boolean(self.show_new_badge),
        }


class FogSquareResourceIn(Strict):
    skin: Optional[Num] = None


class FogSquareIn(Strict):
    """Raw fog island square (``fog_island.squares[]``)."""

    id: Num
    kind: str = Field(alias="type")
    type_id: Optional[Num] = None
    highlight: Num
    x: Num
    y: Num
    island_id: Num
    claim_cost: Num
    come_back_cost: Num
    reward_id: Optional[Num] = None
    resource: Optional[FogSquareResourceIn] = None

    def transform(self) -> JsonDict:
        reward: Optional[JsonDict] = None

        if self.kind not in ("NONE", "STEP"):
            reward = {"type": self.kind}

            if self.kind == "CHEST":
                if self.type_id is not None:
                    reward["chest_id"] = self.type_id
            elif self.kind == "RESOURCE":
                if self.resource is not None and self.resource.skin is not None:
                    reward["skin_id"] = self.resource.skin
            elif self.type_id is not None:
                reward["piece_dragon_id"] = self.type_id

        square: JsonDict = {
            "id": self.id,
            "type": self.kind,
            "reward": reward,
            "is_highlight": number_to_boolean(self.highlight),
            "x": self.x,
            "y": self.y,
            "cost": self.claim_cost,
            "come_back_cost": self.come_back_cost,
        }

        return put(square, reward_id=self.reward_id)
