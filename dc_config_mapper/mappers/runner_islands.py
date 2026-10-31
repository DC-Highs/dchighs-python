from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dc_config_mapper.mappers.base import Mapper, MappedResult
from dc_config_mapper.schemas.runner import (
    RunnerIslandIn,
    RunnerMilestoneRewardIn,
    RunnerMissionIn,
    RunnerMissionPoolIn,
    RunnerRewardIn,
)
from dc_config_mapper.utils import array, parse, passthrough


@dataclass
class MappedRunnerIslands(MappedResult):
    islands: List[Dict[str, Any]]
    missions: List[Dict[str, Any]]
    rewards: List[Dict[str, Any]]
    milestone_rewards: List[Dict[str, Any]]
    mission_pools: List[Dict[str, Any]]
    sections: Optional[Any] = None
    parameters: Optional[Any] = None
    obstacles: Optional[Any] = None
    level_chunks: Optional[Any] = None
    level_rewards: Optional[Any] = None
    rewards_config: Optional[Any] = None
    rewards_tiers: Optional[Any] = None
    milestones: Optional[Any] = None


class RunnerIslandsMapper(Mapper):
    """Maps ``config.runner_island``."""

    def map(self, section: Any) -> MappedRunnerIslands:
        """``section`` is the ``runner_island`` section."""
        return MappedRunnerIslands(
            islands=[
                self.translated(parse("runner island", RunnerIslandIn, island).transform())
                for island in array(section, "islands")
            ],
            missions=[
                self.translated(parse("runner island mission", RunnerMissionIn, mission).transform())
                for mission in array(section, "missions")
            ],
            rewards=[
                parse("runner island reward", RunnerRewardIn, reward).transform()
                for reward in array(section, "rewards")
            ],
            milestone_rewards=[
                parse("runner island milestone reward", RunnerMilestoneRewardIn, reward).transform()
                for reward in array(section, "milestone_rewards")
            ],
            mission_pools=[
                parse("runner island mission pool", RunnerMissionPoolIn, pool).transform()
                for pool in array(section, "mission_pool")
            ],
            sections=passthrough(section, "sections"),
            parameters=passthrough(section, "parameters"),
            obstacles=passthrough(section, "obstacles"),
            level_chunks=passthrough(section, "level_chunks"),
            level_rewards=passthrough(section, "level_rewards"),
            rewards_config=passthrough(section, "rewards_config"),
            rewards_tiers=passthrough(section, "rewards_tiers"),
            milestones=passthrough(section, "milestones"),
        )
