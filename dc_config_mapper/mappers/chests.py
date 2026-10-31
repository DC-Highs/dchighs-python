from typing import Any, Dict, List

from dc_config_mapper.errors import RewardNotFoundError
from dc_config_mapper.mappers.base import Mapper
from dc_config_mapper.schemas.chests import ChestIn, ChestRewardIn
from dc_config_mapper.utils import array, is_number, parse


class ChestsMapper(Mapper):
    """Maps ``config.chests``: resolves the reward ids of every chest and translates names."""

    def map(self, section: Any) -> List[Dict[str, Any]]:
        """``section`` is the ``chests`` section (``{ chests: [...], rewards: [...] }``)."""
        chests = array(section, "chests")
        rewards = array(section, "rewards")

        rewards_by_id: Dict[str, Any] = {}

        for reward in rewards:
            reward_id = reward.get("id") if isinstance(reward, dict) else None

            if is_number(reward_id):
                rewards_by_id.setdefault(str(reward_id), reward)

        mapped = []

        for raw in chests:
            chest: ChestIn = parse("chest", ChestIn, raw)
            resolved = []

            for reward_id in chest.rewards:
                reward = rewards_by_id.get(str(reward_id))

                if reward is None:
                    raise RewardNotFoundError(reward_id)

                resolved.append(parse("chest reward", ChestRewardIn, reward).transform())

            mapped.append(self.translated(chest.transform(resolved)))

        return mapped
