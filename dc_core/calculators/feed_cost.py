from dc_core.settings.feed_costs import FEED_COST_SETTINGS
from dc_core.tools.validation import ValidationError, validate_dragon_level


class InitialLevelHigherThanFinalError(ValidationError):
    def __init__(self) -> None:
        super().__init__("Initial dragon level cannot be higher than final dragon level.")


def calculate_dragon_feed_cost(initial_level: int, final_level: int) -> int:
    """Total food needed to take a dragon from ``initial_level`` to ``final_level``."""
    validate_dragon_level(initial_level)
    validate_dragon_level(final_level)

    if initial_level > final_level:
        raise InitialLevelHigherThanFinalError()

    total_cost = 0

    for level in range(initial_level, final_level):
        total_cost += FEED_COST_SETTINGS[level].total

    return total_cost
