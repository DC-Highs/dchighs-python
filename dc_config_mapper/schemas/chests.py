from typing import Any, List, Optional

from pydantic import Field

from dc_config_mapper.schemas.base import Loose, Strict, dump
from dc_config_mapper.utils import JsonDict, Num, process_rewards, put


class Seed(Loose):
    id: Num
    amount: Num


class RaritySeed(Loose):
    rarity: str
    amount: Num


class BattlegroundKey(Loose):
    battleground_id: Num
    key_id: Num
    amount: Num


class ChestResourceIn(Loose):
    """``reward.resource`` of a chest reward. Field order matters: it is the order
    in which :func:`process_rewards` looks for the ``*_token`` key."""

    p_token: Optional[Num] = None
    f: Optional[Num] = None
    l_token: Optional[Num] = None
    g: Optional[Num] = None
    d_token: Optional[Num] = None
    c: Optional[Num] = None
    i_token: Optional[Num] = None
    pr_token: Optional[Num] = None
    pu_token: Optional[Num] = None
    wr_token: Optional[Num] = None
    e_token: Optional[Num] = None
    f_token: Optional[Num] = None
    w_token: Optional[Num] = None
    el_token: Optional[Num] = None
    m_token: Optional[Num] = None
    li_token: Optional[Num] = None
    ep: Optional[Num] = None
    x: Optional[Num] = None


class ChestRewardBodyIn(Loose):
    resource: Optional[ChestResourceIn] = None
    buildings: Optional[List[Num]] = None
    eggs: Optional[List[Num]] = None
    seeds: Optional[List[Seed]] = None
    moves: Optional[Num] = None
    rarity_seeds: Optional[List[RaritySeed]] = None
    skin: Optional[List[Num]] = None
    battleground_keys: Optional[List[BattlegroundKey]] = None


class ChestRewardIn(Strict):
    """Raw chest reward (``chests.rewards[]``)."""

    id: Num
    reward: ChestRewardBodyIn
    tier_multi: Num
    weight: Num

    def transform(self) -> JsonDict:
        body = self.reward
        resource = None

        if body.resource is not None:
            processed = process_rewards([dump(body.resource)])
            resource = processed[0] if processed else None

        reward = put(
            {},
            resource=resource,
            building_ids=body.buildings,
            eggs_ids=body.eggs,
            seeds=[dump(seed) for seed in body.seeds] if body.seeds is not None else None,
            moves=body.moves,
            rarity_seeds=[dump(seed) for seed in body.rarity_seeds] if body.rarity_seeds is not None else None,
            skin_ids=body.skin,
            battleground_keys=(
                [dump(key) for key in body.battleground_keys] if body.battleground_keys is not None else None
            ),
        )

        return {
            "id": self.id,
            "reward": reward,
            "tier_multi": self.tier_multi,
            "weight": self.weight,
        }


class ChestIn(Strict):
    """Raw chest (``chests.chests[]``) whose ``rewards`` are still reward ids."""

    id: Num
    kind: str = Field(alias="type")
    rewards: List[Num]
    img_name: str
    chest_name_key: str
    type_name_key: str
    level_tiers: List[Num]
    description_key: Optional[str] = None
    default_reward: Num
    pool_size: Num
    gatcha_ids: Optional[List[Num]] = None
    instant: Any = None
    foreground_asset: Optional[str] = None

    def transform(self, rewards: List[JsonDict]) -> JsonDict:
        chest: JsonDict = {
            "id": self.id,
            "type": self.kind,
            "rewards": rewards,
            "image_name": self.img_name,
            "name_key": self.chest_name_key,
            "type_name_key": self.type_name_key,
            "level_tier_ids": self.level_tiers,
        }

        return put(
            chest,
            description_key=self.description_key,
            default_reward_id=self.default_reward,
            pool_size=self.pool_size,
            gatcha_ids=self.gatcha_ids,
            foreground_asset=self.foreground_asset,
        )
