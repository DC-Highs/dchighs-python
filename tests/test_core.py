import pytest

from dc_core import (
    ConfigFilter,
    ConfigLanguage,
    ConfigPlatform,
    DragonAttackStats,
    DragonCategory,
    DragonElement,
    DragonPhase,
    DragonRank,
    DragonStaticFileUrlParser,
    SpriteQuality,
    StaticFileUrlPlatformPrefix,
    TextureCompressionFormat,
    ValidationError,
    calculate_attack_damage,
    calculate_breeding_results,
    calculate_dragon_feed_cost,
    calculate_element_strengths,
    calculate_element_weaknesses,
    calculate_orb_recall_gain,
    get_music_name_from_tag,
    validate_dragon_level_compatibility_with_stars,
    validate_dragon_rarity,
    validate_element_name,
)
from dc_core.calculators import BreedingSource


def test_enum_roundtrip():
    assert ConfigLanguage("tr") is ConfigLanguage.TURKISH
    assert ConfigFilter.DEITY_WORLD_DRAGONS.value == "deity_world_dragons"
    assert str(SpriteQuality.LARGE) == "@2x" == f"{SpriteQuality.LARGE}"

    with pytest.raises(ValueError):
        ConfigFilter("nope")


def test_element_acronyms_are_unique_and_reversible():
    acronyms = [element.acronym for element in DragonElement]
    assert len(set(acronyms)) == len(acronyms)

    for element in DragonElement:
        assert DragonElement.from_acronym(element.acronym) is element

    assert DragonElement.from_acronym("zzz") is None


def test_defaults_match_the_typescript_package():
    assert ConfigLanguage.default().value == "en"
    assert ConfigPlatform.default().value == "ios"
    assert StaticFileUrlPlatformPrefix.default().value == "dci"
    assert TextureCompressionFormat.default().value == "dxt5"


def test_feed_cost_calculator():
    assert calculate_dragon_feed_cost(10, 10) == 0
    assert calculate_dragon_feed_cost(1, 5) == 20 + 40 + 80 + 120

    with pytest.raises(ValidationError):
        calculate_dragon_feed_cost(15, 10)

    with pytest.raises(ValidationError):
        calculate_dragon_feed_cost(0, 10)


def test_orb_recall_gain():
    gain_0_stars = calculate_orb_recall_gain(30)
    assert gain_0_stars > 0
    assert calculate_orb_recall_gain(70, 5) > gain_0_stars


def test_element_calculators():
    strengths = calculate_element_strengths(DragonElement.TERRA)
    assert DragonElement.FLAME in strengths and DragonElement.ELECTRIC in strengths

    weaknesses = calculate_element_weaknesses(DragonElement.TERRA)
    assert DragonElement.METAL in weaknesses and DragonElement.WAR in weaknesses


def test_attack_damage_calculator():
    result = calculate_attack_damage(
        DragonAttackStats(category=DragonCategory.HEROIC, level=70, rank=DragonRank.PLATINUM_I, stars=5),
        1000.0,
    )

    assert result.minimum > 0
    assert result.maximum >= result.minimum
    assert result.minimum <= result.average <= result.maximum
    assert result.minimum <= result.random <= result.maximum


def test_validation():
    with pytest.raises(ValidationError):
        validate_dragon_level_compatibility_with_stars(41, 0)

    with pytest.raises(ValidationError):
        validate_dragon_level_compatibility_with_stars(50, 1)

    validate_dragon_level_compatibility_with_stars(45, 1)
    assert validate_dragon_rarity("c", use_lower_case=True).value == "C"
    assert validate_element_name("TERRA") is DragonElement.TERRA

    with pytest.raises(ValidationError):
        validate_element_name("nope")


def test_url_parser():
    url = "https://dci-static-s1.socialpointgames.com/dragoncity/mobile/ui/dragons/ui_1000_dragon_terra_0@2x.png"
    parsed = DragonStaticFileUrlParser.parse_from_sprite(url)

    assert parsed.platform_prefix is StaticFileUrlPlatformPrefix.IOS
    assert parsed.id == 1000
    assert parsed.phase is DragonPhase.EGG
    assert parsed.image_name == "1000_dragon_terra"
    assert parsed.image_quality is SpriteQuality.LARGE


def test_music_tag_lookup():
    assert get_music_name_from_tag("labyrinth_island_2015") is not None
    assert get_music_name_from_tag("definitely-not-a-tag") is None


def test_breeding_results():
    config = {
        "breeding": [
            {
                "element_one": "f", "element_two": "e",
                "dragon_id_1": 10, "empower_1": 0,
                "dragon_id_2": 11, "empower_2": 1,
                "dragon_id_3": 12, "empower_3": 2,
            }
        ],
        "incompatibilities": [{"element_one": "x", "element_two": "y"}],
        "soulmates": [{"parent_1_id": 1, "parent_2_id": 2, "dragon_id": 11, "chance": 0.5, "level_parents": 10}],
        "special_breeding": [{"condition1": {"id": [1]}, "condition2": {"id": [2]}, "result": 99}],
        "sanctuary_unlocked_dragons": [12],
    }
    parent1 = {"id": 1, "elements": ["f"], "level": 20}
    parent2 = {"id": 2, "elements": ["e"], "level": 20}

    results = {item.dragon_id: item for item in calculate_breeding_results(parent1, parent2, config)}

    assert set(results) == {10, 11, 12, 99}
    assert results[99].sources == [BreedingSource.SPECIAL]
    assert results[11].sources == [BreedingSource.SOULMATE, BreedingSource.REGULAR]
    assert results[11].chance == 0.5 and results[11].required_empower == 1
    assert results[12].sources == [BreedingSource.SANCTUARY]
    assert results[10].to_dict() == {"dragon_id": 10, "sources": ["regular"], "required_empower": 0}

    # Incompatible elements and low parent levels produce nothing.
    parent1["elements"] = ["x"]
    parent2["elements"] = ["y"]
    parent2["level"] = 1
    assert [item.dragon_id for item in calculate_breeding_results(parent1, parent2, config)] == [99]
