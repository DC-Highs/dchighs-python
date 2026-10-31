from typing import Optional

from pydantic import Field

from dc_config_mapper.schemas.base import Strict
from dc_config_mapper.utils import JsonDict, Num, put
from dc_core import DragonElement


class AttackIn(Strict):
    """Raw attack (``skills.attacks[]``)."""

    id: Num
    name: str
    name_key: str
    kind: str = Field(alias="type")
    element: str
    damage: Num
    ui_damage: Num
    effect_atk: Optional[str] = None
    effect_def: str
    effect_sfx: Num
    training_time: Num
    button_style: Num
    special_icon: Num
    skill_id: Optional[Num] = None

    def transform(self) -> JsonDict:
        element = DragonElement.from_acronym(self.element)

        attack: JsonDict = {"id": self.id, "name": self.name, "name_key": self.name_key}

        put(
            attack,
            element=element.value if element is not None else None,
            damage=self.damage,
            ui_damage=self.ui_damage,
            effect_atk=self.effect_atk,
            effect_def=self.effect_def,
            effect_sfx=self.effect_sfx,
            training_time=self.training_time,
            button_style=self.button_style,
            special_icon=self.special_icon,
            skill_id=self.skill_id,
        )

        return attack
