from typing import Dict, NamedTuple, Tuple

from dc_core.enums import DragonElement


class ElementInfo(NamedTuple):
    acronym: str
    name_key: str
    strengths: Tuple[DragonElement, ...]
    weaknesses: Tuple[DragonElement, ...]


ELEMENT_INFO: Dict[DragonElement, ElementInfo] = {
    DragonElement.TERRA: ElementInfo("e", "TerraKey_DragonUtils", (DragonElement.ELECTRIC, DragonElement.FLAME), (DragonElement.METAL, DragonElement.WAR)),
    DragonElement.FLAME: ElementInfo("f", "FlameKey_DragonUtils", (DragonElement.NATURE, DragonElement.ICE), (DragonElement.SEA, DragonElement.TERRA)),
    DragonElement.SEA: ElementInfo("w", "SeaKey_DragonUtils", (DragonElement.FLAME, DragonElement.WAR), (DragonElement.NATURE, DragonElement.ELECTRIC)),
    DragonElement.NATURE: ElementInfo("p", "NatureKey_DragonUtils", (DragonElement.SEA, DragonElement.LIGHT), (DragonElement.FLAME, DragonElement.ICE)),
    DragonElement.ELECTRIC: ElementInfo("el", "ElectricKey_DragonUtils", (DragonElement.SEA, DragonElement.METAL), (DragonElement.TERRA, DragonElement.LIGHT)),
    DragonElement.ICE: ElementInfo("i", "IceKey_DragonUtils", (DragonElement.NATURE, DragonElement.WAR), (DragonElement.FLAME, DragonElement.METAL)),
    DragonElement.METAL: ElementInfo("m", "MetalKey_DragonUtils", (DragonElement.TERRA, DragonElement.ICE), (DragonElement.ELECTRIC, DragonElement.DARK)),
    DragonElement.DARK: ElementInfo("d", "DarkKey_DragonUtils", (DragonElement.METAL, DragonElement.LIGHT), (DragonElement.WAR,)),
    DragonElement.LIGHT: ElementInfo("li", "LightKey_DragonUtils", (DragonElement.ELECTRIC, DragonElement.DARK), (DragonElement.NATURE,)),
    DragonElement.WAR: ElementInfo("wr", "WarKey_DragonUtils", (DragonElement.TERRA, DragonElement.DARK), (DragonElement.SEA, DragonElement.ICE)),
    DragonElement.PURE: ElementInfo("pu", "PureKey_DragonUtils", (DragonElement.WIND,), (DragonElement.PRIMAL,)),
    DragonElement.LEGEND: ElementInfo("l", "LegendKey_DragonUtils", (DragonElement.PRIMAL,), (DragonElement.PURE,)),
    DragonElement.PRIMAL: ElementInfo("pr", "tid_nw_hud_element_primal", (DragonElement.PURE,), (DragonElement.TIME,)),
    DragonElement.WIND: ElementInfo("wd", "tid_nw_hud_element_wind", (DragonElement.TIME,), (DragonElement.LEGEND,)),
    DragonElement.TIME: ElementInfo("ti", "tid_nw_hud_element_time", (DragonElement.LEGEND,), (DragonElement.WIND,)),
    DragonElement.HAPPY: ElementInfo("hp", "tid_nw_hud_element_happiness", (DragonElement.CHAOS, DragonElement.MAGIC), ()),
    DragonElement.CHAOS: ElementInfo("ch", "tid_nw_hud_element_chaos", (DragonElement.MAGIC, DragonElement.SOUL), ()),
    DragonElement.MAGIC: ElementInfo("mg", "tid_nw_hud_element_magic", (DragonElement.SOUL, DragonElement.BEAUTY), ()),
    DragonElement.SOUL: ElementInfo("so", "tid_nw_hud_element_soul", (DragonElement.DREAM, DragonElement.BEAUTY), ()),
    DragonElement.BEAUTY: ElementInfo("bt", "tid_nw_hud_element_beauty", (DragonElement.DREAM, DragonElement.HAPPY), ()),
    DragonElement.DREAM: ElementInfo("dr", "tid_nw_hud_element_dream", (DragonElement.HAPPY, DragonElement.CHAOS), ()),
    DragonElement.PHYSICAL: ElementInfo("ph", "Physical", (), (DragonElement.LEGEND,)),
}


def element_info(element: DragonElement) -> ElementInfo:
    return ELEMENT_INFO[element]
