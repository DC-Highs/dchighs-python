from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Union

from dc_core.enums import StringEnum

_DRAGON_SLOTS = range(1, 8)


@dataclass
class BreedingParent:
    id: int
    elements: List[str]
    level: int
    empower_level: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BreedingParent":
        return cls(
            id=data["id"],
            elements=list(data["elements"]),
            level=data["level"],
            empower_level=data.get("empower_level"),
        )


@dataclass
class BreedingRule:
    element_one: str
    element_two: str
    dragon_id_1: int
    empower_1: int
    dragon_id_2: int
    empower_2: int
    dragon_id_3: int
    empower_3: int
    dragon_id_4: Optional[int] = None
    empower_4: Optional[int] = None
    dragon_id_5: Optional[int] = None
    empower_5: Optional[int] = None
    dragon_id_6: Optional[int] = None
    empower_6: Optional[int] = None
    dragon_id_7: Optional[int] = None
    empower_7: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BreedingRule":
        names = cls.__dataclass_fields__.keys()
        return cls(**{name: data[name] for name in names if name in data})

    def pairs(self) -> List[tuple]:
        """``(dragon_id, empower)`` of the 7 slots (missing optional slots are ``(0, 0)``)."""
        return [
            (getattr(self, f"dragon_id_{slot}") or 0, getattr(self, f"empower_{slot}") or 0)
            for slot in _DRAGON_SLOTS
        ]


@dataclass
class Incompatibility:
    element_one: str
    element_two: str

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Incompatibility":
        return cls(element_one=data["element_one"], element_two=data["element_two"])


@dataclass
class SoulmateRule:
    parent_1_id: int
    parent_2_id: int
    dragon_id: int
    chance: float
    level_parents: int

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SoulmateRule":
        return cls(
            parent_1_id=data["parent_1_id"],
            parent_2_id=data["parent_2_id"],
            dragon_id=data["dragon_id"],
            chance=data["chance"],
            level_parents=data["level_parents"],
        )


@dataclass
class ConditionWithIds:
    id: List[int]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ConditionWithIds":
        return cls(id=list(data["id"]))


@dataclass
class SpecialBreedingRule:
    condition1: ConditionWithIds
    condition2: ConditionWithIds
    result: int

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SpecialBreedingRule":
        return cls(
            condition1=ConditionWithIds.from_dict(data["condition1"]),
            condition2=ConditionWithIds.from_dict(data["condition2"]),
            result=data["result"],
        )


@dataclass
class BreedingConfig:
    breeding: List[BreedingRule] = field(default_factory=list)
    incompatibilities: List[Incompatibility] = field(default_factory=list)
    soulmates: List[SoulmateRule] = field(default_factory=list)
    special_breeding: List[SpecialBreedingRule] = field(default_factory=list)
    sanctuary_unlocked_dragons: List[int] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BreedingConfig":
        return cls(
            breeding=[BreedingRule.from_dict(item) for item in data.get("breeding", [])],
            incompatibilities=[Incompatibility.from_dict(item) for item in data.get("incompatibilities", [])],
            soulmates=[SoulmateRule.from_dict(item) for item in data.get("soulmates", [])],
            special_breeding=[SpecialBreedingRule.from_dict(item) for item in data.get("special_breeding", [])],
            sanctuary_unlocked_dragons=list(data.get("sanctuary_unlocked_dragons", [])),
        )


class BreedingSource(StringEnum):
    SOULMATE = "soulmate"
    SPECIAL = "special"
    SANCTUARY = "sanctuary"
    REGULAR = "regular"


@dataclass
class BreedingResultItem:
    dragon_id: int
    sources: List[BreedingSource]
    required_empower: Optional[int] = None
    chance: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "dragon_id": self.dragon_id,
            "sources": [source.value for source in self.sources],
        }

        if self.required_empower is not None:
            data["required_empower"] = self.required_empower

        if self.chance is not None:
            data["chance"] = self.chance

        return data


def calculate_breeding_results(
    parent1: Union[BreedingParent, Mapping[str, Any]],
    parent2: Union[BreedingParent, Mapping[str, Any]],
    config: Union[BreedingConfig, Mapping[str, Any]],
) -> List[BreedingResultItem]:
    """Every dragon that can come out of breeding ``parent1`` with ``parent2``."""
    if not isinstance(parent1, BreedingParent):
        parent1 = BreedingParent.from_dict(parent1)

    if not isinstance(parent2, BreedingParent):
        parent2 = BreedingParent.from_dict(parent2)

    if not isinstance(config, BreedingConfig):
        config = BreedingConfig.from_dict(config)

    results: Dict[int, BreedingResultItem] = {}

    def add_result(
        dragon_id: int,
        source: BreedingSource,
        empower: Optional[int] = None,
        chance: Optional[float] = None,
    ) -> None:
        if dragon_id == 0:
            return

        existing = results.get(dragon_id)

        if existing is None:
            results[dragon_id] = BreedingResultItem(dragon_id, [source], empower, chance)
            return

        if source not in existing.sources:
            existing.sources.append(source)

        if empower is not None:
            existing.required_empower = (
                empower if existing.required_empower is None else min(existing.required_empower, empower)
            )

        if chance is not None:
            existing.chance = chance if existing.chance is None else max(existing.chance, chance)

    # Special breeding
    for special in config.special_breeding:
        matches_p1_c1 = parent1.id in special.condition1.id
        matches_p2_c2 = parent2.id in special.condition2.id

        matches_p1_c2 = parent1.id in special.condition2.id
        matches_p2_c1 = parent2.id in special.condition1.id

        if (matches_p1_c1 and matches_p2_c2) or (matches_p1_c2 and matches_p2_c1):
            add_result(special.result, BreedingSource.SPECIAL)

    # Soulmates
    for soulmate in config.soulmates:
        matches = (soulmate.parent_1_id == parent1.id and soulmate.parent_2_id == parent2.id) or (
            soulmate.parent_1_id == parent2.id and soulmate.parent_2_id == parent1.id
        )
        levels_match = parent1.level >= soulmate.level_parents and parent2.level >= soulmate.level_parents

        if matches and levels_match:
            add_result(soulmate.dragon_id, BreedingSource.SOULMATE, None, soulmate.chance)

    def is_incompatible(first: str, second: str) -> bool:
        return any(
            (inc.element_one == first and inc.element_two == second)
            or (inc.element_one == second and inc.element_two == first)
            for inc in config.incompatibilities
        )

    for first in parent1.elements:
        for second in parent2.elements:
            if is_incompatible(first, second):
                continue

            rule = next(
                (
                    candidate
                    for candidate in config.breeding
                    if (candidate.element_one == first and candidate.element_two == second)
                    or (candidate.element_one == second and candidate.element_two == first)
                ),
                None,
            )

            if rule is None:
                continue

            for dragon_id, empower in rule.pairs():
                if dragon_id > 0:
                    is_sanctuary = dragon_id in config.sanctuary_unlocked_dragons
                    source = BreedingSource.SANCTUARY if is_sanctuary else BreedingSource.REGULAR
                    add_result(dragon_id, source, empower)

    return list(results.values())
