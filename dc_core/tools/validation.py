from typing import Optional

from dc_core.enums import DragonCategory, DragonElement, DragonRank, DragonRarity
from dc_core.settings.dragons import (
    EMPOWERMENT_STAGES,
    MAXIMUM_LEVEL,
    MAXIMUM_LEVEL_WITHOUT_EMPOWERMENT,
    MAXIMUM_STARS,
    MINIMUM_LEVEL,
    MINIMUM_LEVEL_TO_EMPOWER,
    MINIMUM_STARS,
)


class ValidationError(ValueError):
    """Base class of every validation error of the dragon rules."""


class LevelTooLowError(ValidationError):
    def __init__(self) -> None:
        super().__init__(f"The dragon cannot have a level lower than {MINIMUM_LEVEL}!")


class LevelTooHighError(ValidationError):
    def __init__(self) -> None:
        super().__init__(f"The dragon cannot have a level higher than {MAXIMUM_LEVEL}!")


class StarsTooLowError(ValidationError):
    def __init__(self) -> None:
        super().__init__(f"Dragon stars must be at least {MINIMUM_STARS}!")


class StarsTooHighError(ValidationError):
    def __init__(self) -> None:
        super().__init__(f"Dragon stars cannot exceed {MAXIMUM_STARS}!")


class LevelTooHighForZeroStarsError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            f"Dragon level cannot be higher than {MAXIMUM_LEVEL_WITHOUT_EMPOWERMENT} when stars are 0."
        )


class LevelTooLowForEmpowermentError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            f"Dragon level must be higher than or equal to {MINIMUM_LEVEL_TO_EMPOWER} when stars are not 0."
        )


class StarsExceedStagesError(ValidationError):
    def __init__(self) -> None:
        super().__init__("Dragon stars cannot be higher than the maximum number of empowerment stages.")


class LevelTooHighForStarsError(ValidationError):
    def __init__(self, max_level: int, stars: int) -> None:
        self.max_level = max_level
        self.stars = stars
        super().__init__(f"Dragon level cannot be higher than {max_level} when stars are {stars}.")


class InvalidCategoryError(ValidationError):
    def __init__(self, category: int) -> None:
        self.category = category
        super().__init__(f"Invalid dragon category: {category}.")


class InvalidRankError(ValidationError):
    def __init__(self, rank: int) -> None:
        self.rank = rank
        super().__init__(f"Invalid dragon rank: {rank}.")


class InvalidRarityError(ValidationError):
    def __init__(self, rarity: str) -> None:
        self.rarity = rarity
        super().__init__(f"Invalid dragon rarity: {rarity}.")


class InvalidElementError(ValidationError):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Invalid element name: {name}.")


def validate_dragon_level(level: int) -> None:
    if level < MINIMUM_LEVEL:
        raise LevelTooLowError()
    if level > MAXIMUM_LEVEL:
        raise LevelTooHighError()


def validate_dragon_stars(stars: int) -> None:
    if stars < MINIMUM_STARS:
        raise StarsTooLowError()
    if stars > MAXIMUM_STARS:
        raise StarsTooHighError()


def validate_dragon_level_compatibility_with_stars(level: int, stars: int) -> None:
    validate_dragon_level(level)
    validate_dragon_stars(stars)

    if stars == 0:
        if level > MAXIMUM_LEVEL_WITHOUT_EMPOWERMENT:
            raise LevelTooHighForZeroStarsError()
        return

    if level < MINIMUM_LEVEL_TO_EMPOWER:
        raise LevelTooLowForEmpowermentError()

    if stars > len(EMPOWERMENT_STAGES):
        raise StarsExceedStagesError()

    max_level = EMPOWERMENT_STAGES[stars - 1].dragon_maximum_level

    if level > max_level:
        raise LevelTooHighForStarsError(max_level, stars)


def validate_dragon_category(category: int) -> DragonCategory:
    found = DragonCategory.from_int(category)

    if found is None:
        raise InvalidCategoryError(category)

    return found


def validate_dragon_rank(rank: int) -> Optional[DragonRank]:
    """``None`` for rank ``0`` (unranked)."""
    if rank == 0:
        return None

    found = DragonRank.from_int(rank)

    if found is None:
        raise InvalidRankError(rank)

    return found


def validate_dragon_rarity(rarity: str, use_lower_case: bool = False) -> DragonRarity:
    target = rarity.lower() if use_lower_case else rarity

    for candidate in DragonRarity:
        comparable = candidate.value.lower() if use_lower_case else candidate.value

        if comparable == target:
            return candidate

    raise InvalidRarityError(rarity)


def validate_element_name(element_name: str) -> DragonElement:
    lowered = element_name.lower()

    for element in DragonElement:
        if element.value == lowered:
            return element

    raise InvalidElementError(element_name)
