from typing import Iterable, List, Tuple

from dc_core.enums import DragonElement
from dc_core.settings.elements import element_info
from dc_core.tools.validation import validate_element_name


def calculate_element_resistances(element: DragonElement) -> Tuple[DragonElement, ...]:
    return element_info(element).weaknesses


def calculate_element_resistances_by_name(element_name: str) -> Tuple[DragonElement, ...]:
    return calculate_element_resistances(validate_element_name(element_name))


def calculate_element_strengths(element: DragonElement) -> Tuple[DragonElement, ...]:
    return element_info(element).strengths


def calculate_element_strengths_by_name(element_name: str) -> Tuple[DragonElement, ...]:
    return calculate_element_strengths(validate_element_name(element_name))


def calculate_element_weaknesses(element: DragonElement) -> List[DragonElement]:
    """Elements that are strong against ``element``."""
    return [
        candidate
        for candidate in DragonElement
        if element in element_info(candidate).strengths
    ]


def calculate_element_weaknesses_by_name(element_name: str) -> List[DragonElement]:
    return calculate_element_weaknesses(validate_element_name(element_name))


def calculate_elements_strengths(elements: Iterable[DragonElement]) -> List[DragonElement]:
    """Unique strengths of several elements, in order of appearance."""
    result: List[DragonElement] = []

    for element in elements:
        for strength in element_info(element).strengths:
            if strength not in result:
                result.append(strength)

    return result


def calculate_elements_strengths_by_names(element_names: Iterable[str]) -> List[DragonElement]:
    return calculate_elements_strengths([validate_element_name(name) for name in element_names])
