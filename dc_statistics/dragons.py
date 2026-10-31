from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from dc_statistics._json import as_int, as_list, as_str, get, to_camel_dict


@dataclass
class DragonCategoriesStatistics:
    unique_categories_count: int
    dragon_counts_per_category: Dict[int, int]

    def to_dict(self) -> Dict[str, Any]:
        return to_camel_dict(self)


@dataclass
class DragonElementsStatistics:
    unique_elements_count: int
    dragons_with_one_element: int
    dragons_with_two_elements: int
    dragons_with_three_elements: int
    dragons_with_four_elements: int
    dragons_with_other_elements: int
    dragon_counts_per_element: Dict[str, int]

    def to_dict(self) -> Dict[str, Any]:
        return to_camel_dict(self)


@dataclass
class DragonsStatistics:
    total_count: int
    common_count: int
    rare_count: int
    very_rare_count: int
    epic_count: int
    legendary_count: int
    mythical_count: int
    heroic_count: int
    elements: DragonElementsStatistics
    categories: DragonCategoriesStatistics
    breedable_count: int
    in_store_count: int

    def to_dict(self) -> Dict[str, Any]:
        return to_camel_dict(self)


_RARITY_COUNTERS = {
    "C": "common_count",
    "R": "rare_count",
    "V": "very_rare_count",
    "E": "epic_count",
    "L": "legendary_count",
    "M": "mythical_count",
    "H": "heroic_count",
}


def generate_dragons_statistics(dragons: Iterable[Dict[str, Any]]) -> DragonsStatistics:
    """Statistics of the dragon items (the ``items`` whose ``group_type`` is ``DRAGON``)."""
    dragons = list(dragons)
    counts = {counter: 0 for counter in _RARITY_COUNTERS.values()}
    breedable_count = 0
    in_store_count = 0

    for dragon in dragons:
        counter = _RARITY_COUNTERS.get(as_str(get(dragon, "dragon_rarity")) or "")

        if counter is not None:
            counts[counter] += 1

        if as_int(get(dragon, "breedable")) == 1 or as_int(get(dragon, "can_breed")) == 1:
            breedable_count += 1

        if as_int(get(dragon, "in_store")) == 1:
            in_store_count += 1

    return DragonsStatistics(
        total_count=len(dragons),
        elements=generate_dragon_elements_statistics(dragons),
        categories=generate_dragon_categories_statistics(dragons),
        breedable_count=breedable_count,
        in_store_count=in_store_count,
        **counts,
    )


def generate_dragon_categories_statistics(dragons: Iterable[Dict[str, Any]]) -> DragonCategoriesStatistics:
    category_counts: Dict[int, int] = {}

    for dragon in dragons:
        category = as_int(get(dragon, "category"))

        if category is not None and category >= 0:
            category_counts[category] = category_counts.get(category, 0) + 1

    return DragonCategoriesStatistics(
        unique_categories_count=len(category_counts),
        dragon_counts_per_category=category_counts,
    )


def generate_dragon_elements_statistics(dragons: Iterable[Dict[str, Any]]) -> DragonElementsStatistics:
    element_counts: Dict[str, int] = {}
    by_size = {1: 0, 2: 0, 3: 0, 4: 0}
    other = 0

    for dragon in dragons:
        raw = as_list(get(dragon, "attributes")) or []
        attributes: List[str] = [item for item in raw if isinstance(item, str)]

        if len(attributes) in by_size:
            by_size[len(attributes)] += 1
        else:
            other += 1

        for attribute in attributes:
            element_counts[attribute] = element_counts.get(attribute, 0) + 1

    return DragonElementsStatistics(
        unique_elements_count=len(element_counts),
        dragons_with_one_element=by_size[1],
        dragons_with_two_elements=by_size[2],
        dragons_with_three_elements=by_size[3],
        dragons_with_four_elements=by_size[4],
        dragons_with_other_elements=other,
        dragon_counts_per_element=element_counts,
    )
