from typing import NamedTuple, Tuple

from dc_core.enums import DragonCategory, DragonRank

MINIMUM_LEVEL = 1
MAXIMUM_LEVEL = 70
MAXIMUM_LEVEL_WITHOUT_EMPOWERMENT = 40
MINIMUM_LEVEL_TO_EMPOWER = 7

MINIMUM_STARS = 0
MAXIMUM_STARS = 5


class EmpowermentStage(NamedTuple):
    requested_orbs: int
    usable_joker_orbs: int
    dragon_maximum_level: int


EMPOWERMENT_STAGES: Tuple[EmpowermentStage, ...] = (
    EmpowermentStage(120, 25, 45),
    EmpowermentStage(200, 50, 50),
    EmpowermentStage(320, 80, 55),
    EmpowermentStage(560, 170, 60),
    EmpowermentStage(800, 240, 70),
)

ONE_STAR_POWER = 0.38223
DAMAGE_VARIANT = (0.9, 1.1)

_CATEGORY_POWER = {
    DragonCategory.BASIC: 3200.0,
    DragonCategory.PRO_BASIC: 3600.0,
    DragonCategory.PRE_ADVANCED: 4000.0,
    DragonCategory.ADVANCED: 4800.0,
    DragonCategory.ELITE: 5600.0,
    DragonCategory.AMAZING: 5000.0,
    DragonCategory.CHARMING: 4500.0,
    DragonCategory.GRACEFUL: 3000.0,
    DragonCategory.CHAMPION: 6000.0,
    DragonCategory.MYTHICAL: 7300.0,
    DragonCategory.HEROIC: 9000.0,
}

_RANK_POWER = {
    DragonRank.BRONZE_III: 0.05,
    DragonRank.BRONZE_II: 0.10,
    DragonRank.BRONZE_I: 0.15,
    DragonRank.SILVER_III: 0.20,
    DragonRank.SILVER_II: 0.25,
    DragonRank.SILVER_I: 0.30,
    DragonRank.GOLD_III: 0.35,
    DragonRank.GOLD_II: 0.40,
    DragonRank.GOLD_I: 0.50,
    DragonRank.PLATINUM_III: 0.55,
    DragonRank.PLATINUM_II: 0.60,
    DragonRank.PLATINUM_I: 0.70,
}

_RANK_NAME_KEYS = {
    DragonRank.BRONZE_III: "tid_rank_bronze_iii",
    DragonRank.BRONZE_II: "tid_rank_bronze_ii",
    DragonRank.BRONZE_I: "tid_rank_bronze_i",
    DragonRank.SILVER_III: "tid_rank_silver_iii",
    DragonRank.SILVER_II: "tid_rank_silver_ii",
    DragonRank.SILVER_I: "tid_rank_silver_i",
    DragonRank.GOLD_III: "tid_rank_gold_iii",
    DragonRank.GOLD_II: "tid_rank_gold_ii",
    DragonRank.GOLD_I: "tid_rank_gold_i",
    DragonRank.PLATINUM_III: "tid_rank_platinum_iii",
    DragonRank.PLATINUM_II: "tid_rank_platinum_ii",
    DragonRank.PLATINUM_I: "tid_rank_platinum_i",
}


def category_power(category: DragonCategory) -> float:
    return _CATEGORY_POWER[category]


def rank_power(rank: DragonRank) -> float:
    return _RANK_POWER[rank]


def rank_bonus_from_int(rank: int) -> float:
    """Rank bonus of a rank number (``0.0`` for unranked/unknown ranks)."""
    found = DragonRank.from_int(rank)
    return _RANK_POWER[found] if found is not None else 0.0


def rank_name_key(rank: DragonRank) -> str:
    return _RANK_NAME_KEYS[rank]
