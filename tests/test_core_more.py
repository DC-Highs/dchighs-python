import pytest

from dc_core import (
    BreedingConfig,
    BreedingParent,
    BreedingRule,
    BreedingSource,
    ConfigLanguage,
    ConfigPlatform,
    DragonAttackStats,
    DragonCategory,
    DragonElement,
    DragonPhase,
    DragonRank,
    DragonRarity,
    DragonStaticFileUrlParser,
    InvalidCategoryError,
    InvalidElementError,
    InvalidRankError,
    InvalidRarityError,
    LevelTooHighError,
    LevelTooHighForStarsError,
    LevelTooHighForZeroStarsError,
    LevelTooLowError,
    LevelTooLowForEmpowermentError,
    SpriteQuality,
    StarsExceedStagesError,
    StarsTooHighError,
    StarsTooLowError,
    StaticFileUrlPlatformPrefix,
    TextureCompressionFormat,
    calculate_attack_damage,
    calculate_breeding_results,
    calculate_element_resistances,
    calculate_element_resistances_by_name,
    calculate_element_strengths_by_name,
    calculate_element_weaknesses_by_name,
    calculate_elements_strengths,
    calculate_elements_strengths_by_names,
    validate_dragon_category,
    validate_dragon_level,
    validate_dragon_level_compatibility_with_stars,
    validate_dragon_rank,
    validate_dragon_rarity,
    validate_dragon_stars,
)
from dc_core.settings import EMPOWERMENT_STAGES, category_power, rank_bonus_from_int, rank_name_key, rank_power


def test_enum_helpers():
    assert SpriteQuality.default() is SpriteQuality.NORMAL
    assert ConfigPlatform.default() is ConfigPlatform.IOS
    assert StaticFileUrlPlatformPrefix.default() is StaticFileUrlPlatformPrefix.IOS
    assert TextureCompressionFormat.default() is TextureCompressionFormat.DXT5
    assert ConfigLanguage.default() is ConfigLanguage.ENGLISH
    assert SpriteQuality.LARGE.as_str == "@2x"
    assert str(DragonPhase.ADULT) == "3" == f"{DragonPhase.ADULT}"
    assert DragonCategory.from_int(11) is DragonCategory.HEROIC
    assert DragonCategory.from_int(99) is None
    assert DragonRank.from_int(12) is DragonRank.PLATINUM_I
    assert DragonRank.from_int(99) is None
    assert DragonRank.GOLD_I.name_key == "tid_rank_gold_i"
    assert DragonElement.TERRA.strengths == (DragonElement.ELECTRIC, DragonElement.FLAME)
    assert DragonElement.TERRA.weaknesses == (DragonElement.METAL, DragonElement.WAR)
    assert DragonRarity("C") is DragonRarity.COMMON


def test_settings():
    assert category_power(DragonCategory.HEROIC) == 9000.0
    assert rank_power(DragonRank.PLATINUM_I) == 0.7
    assert rank_bonus_from_int(9) == 0.5
    assert rank_bonus_from_int(0) == 0.0
    assert rank_name_key(DragonRank.BRONZE_III) == "tid_rank_bronze_iii"
    assert len(EMPOWERMENT_STAGES) == 5


def test_element_calculators_by_name():
    assert calculate_element_strengths_by_name("terra") == (DragonElement.ELECTRIC, DragonElement.FLAME)
    assert calculate_element_resistances(DragonElement.TERRA) == calculate_element_resistances_by_name("Terra")
    assert DragonElement.METAL in calculate_element_weaknesses_by_name("terra")
    assert calculate_elements_strengths([DragonElement.TERRA, DragonElement.FLAME, DragonElement.METAL]) == [
        DragonElement.ELECTRIC,
        DragonElement.FLAME,
        DragonElement.NATURE,
        DragonElement.ICE,
        DragonElement.TERRA,
    ]
    assert calculate_elements_strengths_by_names(["terra", "flame"]) == [
        DragonElement.ELECTRIC,
        DragonElement.FLAME,
        DragonElement.NATURE,
        DragonElement.ICE,
    ]

    with pytest.raises(InvalidElementError):
        calculate_elements_strengths_by_names(["nope"])


def test_validation_errors():
    with pytest.raises(LevelTooLowError):
        validate_dragon_level(0)

    with pytest.raises(LevelTooHighError):
        validate_dragon_level(71)

    with pytest.raises(StarsTooLowError):
        validate_dragon_stars(-1)

    with pytest.raises(StarsTooHighError):
        validate_dragon_stars(6)

    with pytest.raises(LevelTooHighForZeroStarsError):
        validate_dragon_level_compatibility_with_stars(41, 0)

    with pytest.raises(LevelTooLowForEmpowermentError):
        validate_dragon_level_compatibility_with_stars(6, 1)

    with pytest.raises(LevelTooHighForStarsError) as error:
        validate_dragon_level_compatibility_with_stars(60, 2)

    assert (error.value.max_level, error.value.stars) == (50, 2)

    with pytest.raises(InvalidCategoryError) as category_error:
        validate_dragon_category(99)

    assert category_error.value.category == 99
    assert validate_dragon_category(1) is DragonCategory.BASIC
    assert validate_dragon_rank(0) is None
    assert validate_dragon_rank(3) is DragonRank.BRONZE_I

    with pytest.raises(InvalidRankError):
        validate_dragon_rank(99)

    assert validate_dragon_rarity("C") is DragonRarity.COMMON

    with pytest.raises(InvalidRarityError):
        validate_dragon_rarity("c")

    with pytest.raises(InvalidRarityError):
        validate_dragon_rarity("zzz", use_lower_case=True)


def test_stars_exceeding_the_stages(monkeypatch):
    import dc_core.tools.validation as validation

    monkeypatch.setattr(validation, "MAXIMUM_STARS", 6)

    with pytest.raises(StarsExceedStagesError):
        validate_dragon_level_compatibility_with_stars(50, 6)


def test_attack_damage_without_stars_and_unranked():
    result = calculate_attack_damage(DragonAttackStats(1, 10, 0, 0), 0.0)
    assert result.minimum <= result.average <= result.maximum


def test_url_parser_variants():
    thumb = DragonStaticFileUrlParser.parse_from_thumbnail(
        "https://dca-static-s1.socialpointgames.com/static/dragoncity/mobile/ui/dragons/HD/thumb_1000_dragon_nature_skin2_3.png"
    )
    assert (thumb.platform_prefix, thumb.id, thumb.phase, thumb.skin) == (
        StaticFileUrlPlatformPrefix.ANDROID,
        1000,
        DragonPhase.ADULT,
        "_skin2",
    )

    spine = DragonStaticFileUrlParser.parse_from_spine_animation(
        "https://dci-static-s1.socialpointgames.com/x/1000_dragon_nature_1/1000_dragon_nature_1_HD_tweened_dxt5.zip"
    )
    assert spine.phase is DragonPhase.BABY
    flash = DragonStaticFileUrlParser.parse_from_flash_animation("https://dci-static-s1.x/a_2.swf")
    assert flash.phase is DragonPhase.YOUNG

    assert DragonStaticFileUrlParser.get_platform_prefix("no url") is None
    assert DragonStaticFileUrlParser.get_platform_prefix("https://zzz-static-s1.x") is None
    assert DragonStaticFileUrlParser.get_image_name("nothing") is None
    assert DragonStaticFileUrlParser.get_id("nothing") is None
    assert DragonStaticFileUrlParser.get_phase("nothing") is None
    assert DragonStaticFileUrlParser.get_phase("a_9.png") is None
    assert DragonStaticFileUrlParser.get_skin("nothing") is None
    assert DragonStaticFileUrlParser.get_image_quality("a.png") is SpriteQuality.NORMAL


def rule(first, second, dragon_ids, **extra):
    data = {"element_one": first, "element_two": second}

    for index, dragon_id in enumerate(dragon_ids, start=1):
        data[f"dragon_id_{index}"] = dragon_id
        data[f"empower_{index}"] = index

    data.update(extra)
    return data


def test_breeding_models_and_merging():
    parent = BreedingParent.from_dict({"id": 1, "elements": ["f"], "level": 5, "empower_level": 2})
    assert parent.empower_level == 2

    full = BreedingRule.from_dict(rule("f", "e", [10, 20, 30, 40, 50, 60, 70]))
    assert full.pairs()[-1] == (70, 7)
    assert BreedingRule.from_dict(rule("f", "e", [1, 2, 3])).pairs()[3] == (0, 0)

    config = BreedingConfig(
        breeding=[
            BreedingRule.from_dict(rule("f", "e", [10, 11, 12])),
            BreedingRule.from_dict(rule("e", "f", [10, 11, 12])),
        ],
    )
    parent1 = BreedingParent(1, ["f", "e"], 10)
    parent2 = BreedingParent(2, ["e", "f"], 10)

    results = {item.dragon_id: item for item in calculate_breeding_results(parent1, parent2, config)}

    assert results[10].required_empower == 1
    assert results[10].sources == [BreedingSource.REGULAR]


def test_breeding_merges_sources_empower_and_chance():
    config = {
        "breeding": [rule("f", "e", [10, 0, 0])],
        "soulmates": [
            {"parent_1_id": 1, "parent_2_id": 2, "dragon_id": 10, "chance": 0.2, "level_parents": 1},
            {"parent_1_id": 2, "parent_2_id": 1, "dragon_id": 10, "chance": 0.7, "level_parents": 1},
            {"parent_1_id": 1, "parent_2_id": 2, "dragon_id": 10, "chance": 0.1, "level_parents": 1},
        ],
        "special_breeding": [{"condition1": {"id": [2]}, "condition2": {"id": [1]}, "result": 10}],
        "sanctuary_unlocked_dragons": [10],
    }
    parent1 = {"id": 1, "elements": ["f"], "level": 5}
    parent2 = {"id": 2, "elements": ["e"], "level": 5}

    [item] = calculate_breeding_results(parent1, parent2, config)

    assert item.sources == [BreedingSource.SPECIAL, BreedingSource.SOULMATE, BreedingSource.SANCTUARY]
    assert item.chance == 0.7
    assert item.required_empower == 1

    repeated = {"breeding": [rule("f", "e", [10, 10, 10])]}
    [again] = calculate_breeding_results(parent1, parent2, repeated)
    assert again.required_empower == 1
    assert again.sources == [BreedingSource.REGULAR]
    assert again.to_dict() == {"dragon_id": 10, "sources": ["regular"], "required_empower": 1}
    assert item.to_dict()["chance"] == 0.7

    assert calculate_breeding_results(parent1, parent2, {"breeding": []}) == []
    assert (
        calculate_breeding_results(
            parent1,
            parent2,
            {"special_breeding": [{"condition1": {"id": [1]}, "condition2": {"id": [3]}, "result": 5}]},
        )
        == []
    )
    assert (
        calculate_breeding_results(
            parent1,
            parent2,
            {"special_breeding": [{"condition1": {"id": [1]}, "condition2": {"id": [2]}, "result": 0}]},
        )
        == []
    )


def test_breeding_result_without_extras():
    from dc_core import BreedingResultItem

    assert BreedingResultItem(1, [BreedingSource.SPECIAL]).to_dict() == {"dragon_id": 1, "sources": ["special"]}
