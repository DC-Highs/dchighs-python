import math
import random
from dataclasses import dataclass

from dc_core.settings.dragons import (
    DAMAGE_VARIANT,
    ONE_STAR_POWER,
    category_power,
    rank_bonus_from_int,
)
from dc_core.tools.validation import (
    validate_dragon_category,
    validate_dragon_level_compatibility_with_stars,
    validate_dragon_rank,
)


@dataclass(frozen=True)
class DragonAttackStats:
    category: int
    level: int
    rank: int
    stars: int


@dataclass(frozen=True)
class AttackDamageResult:
    minimum: int
    maximum: int
    average: int
    random: int


def _round(value: float) -> int:
    """Rounds half away from zero (``Math.round``/Rust ``round`` instead of banker's rounding)."""
    return int(math.copysign(math.floor(abs(value) + 0.5), value))


def calculate_attack_damage(dragon: DragonAttackStats, attack_power: float) -> AttackDamageResult:
    validate_dragon_level_compatibility_with_stars(dragon.level, dragon.stars)
    category = validate_dragon_category(dragon.category)
    validate_dragon_rank(dragon.rank)

    initial_damage = category_power(category)
    level_bonus = float(dragon.level) ** 1.5 + 10.0
    rank_bonus = rank_bonus_from_int(dragon.rank)
    stars_bonus = ONE_STAR_POWER * dragon.stars if dragon.stars > 0 else 0.0

    damage = (
        1.5 * (1.0 + rank_bonus + stars_bonus) * (initial_damage * level_bonus / 250.0)
        + attack_power
    )

    minimum = _round(DAMAGE_VARIANT[0] * damage)
    maximum = _round(DAMAGE_VARIANT[1] * damage)
    average = _round((minimum + maximum) / 2.0)

    random_factor = random.uniform(DAMAGE_VARIANT[0], DAMAGE_VARIANT[1])
    random_damage = _round(random_factor * damage)

    return AttackDamageResult(
        minimum=minimum,
        maximum=maximum,
        average=average,
        random=random_damage,
    )
