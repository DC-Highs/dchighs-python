from typing import Optional

from dc_core.settings.orb_recall_return import ORB_RECALL_PER_LEVELS, ORB_RECALL_PER_STARS
from dc_core.tools.validation import validate_dragon_level_compatibility_with_stars


def calculate_orb_recall_gain(level: int, stars: Optional[int] = None) -> int:
    """Orbs given back when recalling a dragon of ``level`` with ``stars`` empowerment stars."""
    adjusted_stars = stars or 0
    validate_dragon_level_compatibility_with_stars(level, adjusted_stars)

    adjusted_level = min(level, 30)
    total_orbs = sum(ORB_RECALL_PER_LEVELS[:adjusted_level])
    total_orbs += sum(ORB_RECALL_PER_STARS[:adjusted_stars])

    return total_orbs
