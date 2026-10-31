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


class GridIslandIn(Strict):
    """Raw grid island (``grid_island.islands[]``).

    ``ui_configuration``/``active_platforms`` are not part of the mapped output, so they are kept as raw JSON.
    """

    id: Num
    analytics_id: str
    tid_name: str
    tutorial_id: Num
    tutorial_claimable_cell_id: Num
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
    ui_configuration: Any
    active_platforms: Any
    episodes: List[Num]
    board_size: List[Num]
    initial_square_id: Num
    backgrounds: List[Num]
    background_plist: str
    foregrounds: List[Any]
    foregrounds_plists: List[Any]

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "min_level": self.min_level,
            "availability": availability_from_ts(self.start_ts, self.end_ts),
            "name_key": self.tid_name,
            "sound_tag": self.sound_tag,
            "zip_file_name": basename(self.zip_file),
            "currency_id": self.currency_id,
            "pool": {"points": self.pool_points, "time": self.pool_time},
            "initial_points": self.initial_points,
            "board_size": size_from_pair(self.board_size),
            "initial_square_id": self.initial_square_id,
            "episode_ids": self.episodes,
        }


class GridEpisodeIn(Strict):
    """Raw grid episode (``grid_island.episodes[]``) plus the injected ``decoration_ids``."""

    id: Num
    island_id: Num
    board_size: List[Num]
    initial_square_id: Num
    final_square_id: Num
    tid_title: str
    mobile_begin_tutorial_id: Num
    mobile_end_tutorial_id: Num
    canvas_background: str
    backgrounds: List[str]
    background_plist: str
    foregrounds: List[Any]
    foregrounds_plists: List[Any]
    squares: List[Num]
    decoration_ids: List[Num]

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "board_size": size_from_pair(self.board_size),
            "initial_square_id": self.initial_square_id,
            "final_square_id": self.final_square_id,
            "name_key": self.tid_title,
            "square_ids": self.squares,
            "decoration_ids": self.decoration_ids,
        }


class GridSquareIn(Strict):
    """Raw grid square (``grid_island.squares[]``)."""

    id: Num
    kind: str = Field(alias="type")
    type_id: Optional[Num] = None
    highlight: Num
    x: Num
    y: Num
    island_id: Num
    episode_id: Num
    claim_cost: Num
    wall: Optional[str] = None
    wall_suffix: Optional[str] = None
    resource: Optional[Any] = None

    def transform(self) -> JsonDict:
        reward: Optional[JsonDict] = None

        if self.kind != "NONE":
            reward = {"type": self.kind.lower()}

            if self.type_id is not None:
                reward["chest_id" if self.kind == "CHEST" else "dragon_id"] = self.type_id

        square: JsonDict = {
            "id": self.id,
            "type": self.kind,
            "reward": reward,
            "is_highlight": number_to_boolean(self.highlight),
            "x": self.x,
            "y": self.y,
            "cost": self.claim_cost,
        }

        return put(square, wall=self.wall, wall_suffix=self.wall_suffix, resource=self.resource)


class GridDecorationIn(Strict):
    """Raw grid decoration (``grid_island.decorations[]``)."""

    id: Num
    file: str
    x: Num
    y: Num
    island_id: Num
    episode_id: Num

    def transform(self) -> JsonDict:
        return {"id": self.id, "file_name": f"{self.file}.png", "x": self.x, "y": self.y}


class GridEncounterIn(Strict):
    """Raw grid encounter (``grid_island.encounters[]``)."""

    id: Num
    enemies: List[Num]
    speed_up_price_per_hour: Num
    fight_background: str
    fight_background_id: str

    def transform(self) -> JsonDict:
        return {
            "id": self.id,
            "enemy_ids": self.enemies,
            "speed_up_price_per_hour": self.speed_up_price_per_hour,
            "fight_background": self.fight_background,
            "fight_background_id": self.fight_background_id,
        }
