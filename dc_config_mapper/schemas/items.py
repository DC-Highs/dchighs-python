from typing import Any, List, Optional

from pydantic import Field

from dc_config_mapper.schemas.base import Loose, Strict
from dc_config_mapper.utils import JsonDict, Num, number_to_boolean, process_price, put
from dc_core import DragonElement


class Costs(Loose):
    c: Optional[Num] = None
    g: Optional[Num] = None

    def price(self) -> Optional[JsonDict]:
        return process_price(self.c, self.g)


class GoldPrice(Loose):
    g: Optional[Num] = None


class RequiredGoldPrice(Loose):
    g: Num


class DragonIn(Strict):
    """Raw dragon (``items`` with ``group_type == "DRAGON"``)."""

    id: Num
    name: str
    group_type: str
    speed: Num
    mobile_version: Num
    android_version: Num
    display_order: Num
    hatching_time: Num
    breeding_time: Num
    xp: Num
    lvl: Num
    costs: Costs
    sell_price: RequiredGoldPrice
    starting_coins: Num
    coins_added: Num
    can_breed: Num
    breedable: Num
    deity_breeding: Num
    difficulty: Num
    category: Num
    rarity: Num
    dragon_rarity: str
    attacks: List[Num]
    attributes: List[str]
    trainable_attacks: List[Num]
    upgrade_levels: List[Num]
    background_vfx: List[Num]
    foreground_vfx: List[Num]
    in_store: Num
    in_store_min_level: Num
    flying_level: Num
    swim: Num
    new_item: Num
    img_name: Optional[str] = None
    img_name_mobile: Optional[str] = None
    img_name_android: Optional[str] = None
    giftable: Optional[Num] = None
    gift_level: Num
    description: Optional[str] = None
    seeds_to_summon: Num
    hatching_time_10: Num
    breeding_time_40: Num
    breeding_time_10: Num
    hatching_time_40: Num
    base_attack: Num
    base_life: Num
    in_store_ch: Optional[Num] = None
    costs_ch_1: Optional[Costs] = None
    costs_ch_2: Optional[Costs] = None
    hatching_time_reawaken: Optional[Num] = None
    breeding_time_reawaken: Optional[Num] = None
    hatching_time_ngu_aggressive: Optional[Num] = None
    breeding_time_ngu_aggressive: Optional[Num] = None
    hatching_time_ngu_soft: Optional[Num] = None
    breeding_time_ngu_soft: Optional[Num] = None
    dragon_ownership_id: Num
    tags: Optional[List[str]] = None
    speed_override: Optional[Num] = None
    passive_skills: Optional[List[Num]] = None
    post_skills: Optional[List[Num]] = None

    def transform(self) -> JsonDict:
        elements = [
            element.value if element is not None else None
            for element in (DragonElement.from_acronym(acronym) for acronym in self.attributes)
        ]

        stats: JsonDict = {
            "attack": self.base_attack,
            "life": self.base_life,
            "speed": self.speed,
            "level": self.lvl,
        }
        put(stats, speed_override=self.speed_override)

        hatching: JsonDict = {"default": self.hatching_time}
        put(
            hatching,
            hatching_reawaken=self.hatching_time_reawaken,
            hatching_ngu_aggressive=self.hatching_time_ngu_aggressive,
            hatching_ngu_soft=self.hatching_time_ngu_soft,
        )

        breeding: JsonDict = {"default": self.breeding_time}
        put(
            breeding,
            breeding_reawaken=self.breeding_time_reawaken,
            breeding_ngu_aggressive=self.breeding_time_ngu_aggressive,
            breeding_ngu_soft=self.breeding_time_ngu_soft,
        )

        dragon: JsonDict = {
            "id": self.id,
            "name": self.name,
            "name_key": f"tid_unit_{self.id}_name",
            "rarity": self.dragon_rarity,
            "elements": elements,
        }

        put(dragon, description=self.description)

        dragon.update(
            {
                "description_key": f"tid_unit_{self.id}_description",
                "buy_price": self.costs.price(),
                "sell_price": process_price(None, self.sell_price.g),
                "is_breedable": number_to_boolean(self.breedable),
                "can_breed": number_to_boolean(self.can_breed),
                "is_in_store": number_to_boolean(self.in_store),
                "min_store_level": self.in_store_min_level,
                "basic_attack_ids": self.attacks,
                "trainable_attack_ids": self.trainable_attacks,
                "passive_skill_ids": self.passive_skills,
                "post_skill_ids": self.post_skills,
                "category": self.category,
                "stats": stats,
                "timers": {"hatching": hatching, "breeding": breeding},
                "production": {"coins_added": self.coins_added, "starting_coins": self.starting_coins},
                "xp_on_hatch": self.xp,
                "seeds_to_summon": self.seeds_to_summon,
                "upgrade_phase_levels": self.upgrade_levels,
                "image_names": {
                    "default": self.img_name,
                    "mobile": self.img_name_mobile,
                    "android": self.img_name_android,
                },
                "tags": self.tags if self.tags is not None else [],
            }
        )

        return dragon


class BuildingProperties(Loose):
    """``properties`` of a building. Unknown keys are dropped, like zod does for non-strict objects."""

    capacity: Optional[Num] = None
    incubator: Optional[Num] = None
    bulldozable: Optional[Num] = None
    max_dragon_level: Optional[Num] = None
    required_items: Optional[List[Num]] = None
    working_building: Optional[Num] = Field(default=None, alias="workingBuilding")
    breeding: Optional[Num] = None
    breeding_factor: Optional[Num] = None
    max_gold: Optional[Num] = None
    friend_assistable: Optional[Num] = None
    upgrade_from: Optional[Num] = None
    floating: Optional[Num] = None
    fixed_position: Optional[List[Num]] = None
    is_fixed: Optional[Num] = None
    crosspromotion: Optional[Num] = None
    ft_flying: Optional[Num] = None


class BuildingIn(Strict):
    """Raw building (``items`` with ``group_type == "BUILDING"``)."""

    id: Num
    name: str
    group_type: str
    name_key: Optional[str] = None
    animated: Num
    build_time: Num
    mobile_version: Num
    android_version: Num
    show_on_mobile: Num
    kind: str = Field(alias="type")
    element_type: Optional[str] = None
    xp: Num
    min_level: Num
    costs: Costs
    display_order: Num
    boost_modifier: Num
    gift_level: Num
    giftable: Num
    cost_unit_cash: Optional[Num] = None
    collect: Num
    collect_xp: Optional[Num] = None
    category_id: Num
    subcategory_id: Num
    building_limit_same_id: Num
    in_store: Num
    width: Num
    height: Num
    new_item: Num
    img_name: str
    img_name_mobile: str
    img_name_android: str
    activation: Num
    upgrades_to: Num
    collect_type: Optional[Any] = None
    velocity: Num
    description: Optional[str] = None
    properties: BuildingProperties
    building_ownership_id: Num
    sell_price: Optional[GoldPrice] = None
    inventory_ids: Optional[Num] = None

    def transform(self) -> JsonDict:
        sell_price = process_price(None, self.sell_price.g) if self.sell_price is not None else None

        building: JsonDict = {"id": self.id, "name": self.name}

        put(building, name_key=self.name_key)

        building.update(
            {
                "animated": number_to_boolean(self.animated),
                "build_time": self.build_time,
                "type": self.kind,
            }
        )

        put(building, element_type=self.element_type)

        building.update(
            {
                "xp_on_build": self.xp,
                "min_level": self.min_level,
                "buy_price": self.costs.price(),
                "display_order": self.display_order,
                "boost_modifier": self.boost_modifier,
            }
        )

        put(building, cost_unit_cash=self.cost_unit_cash)
        building["collect"] = self.collect
        put(building, collect_xp=self.collect_xp)

        building.update(
            {
                "category_id": self.category_id,
                "subcategory_id": self.subcategory_id,
                "building_limit_same_id": self.building_limit_same_id,
                "in_store": number_to_boolean(self.in_store),
                "width": self.width,
                "height": self.height,
                "new_item": number_to_boolean(self.new_item),
                "imageNames": {
                    "default": self.img_name,
                    "mobile": self.img_name_mobile,
                    "android": self.img_name_android,
                },
                "activation": self.activation,
                "upgrades_to": self.upgrades_to,
            }
        )

        put(building, collect_type=self.collect_type)
        building["velocity"] = self.velocity
        put(building, description=self.description)

        building.update(
            {
                "properties": self.properties.model_dump(by_alias=True, exclude_none=True),
                "building_ownership_id": self.building_ownership_id,
                "sell_price": sell_price,
            }
        )

        put(building, inventory_ids=self.inventory_ids)
        return building
