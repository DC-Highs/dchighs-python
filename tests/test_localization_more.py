import httpx
import pytest

from dc_core import ConfigLanguage
from dc_localization import LanguageMismatchError, Localization, LocalizationHttpError, NormalizeOptions


def localization() -> Localization:
    return Localization(
        ConfigLanguage.ENGLISH,
        {
            "tid_unit_1_name": "Dragon",
            "tid_unit_1_description": "A dragon",
            "tid_attack_name_2": "Bite",
            "tid_skill_name_3": "Roar",
            "tid_skill_description_3": "Loud",
            "tid_empty": "",
            "Key_Upper": "  Ação  ",
        },
    )


def test_lookups():
    loc = localization()

    assert loc.get_value_from_key("missing") is None
    assert loc.get_key_from_value("Nope") is None
    assert loc.get_dragon_description(1) == "A dragon"
    assert loc.get_attack_name(2) == "Bite"
    assert loc.get_skill_name(3) == "Roar"
    assert loc.get_skill_description(3) == "Loud"
    assert "dragons" not in repr(loc) and "entries=7" in repr(loc)
    assert Localization(ConfigLanguage.FRENCH, {}).url.endswith("dc_android_fr_prod_wetd46pWuR8J5CmS.json")


def test_search_options():
    loc = localization()

    assert loc.search_keys("key_upper") == ["Key_Upper"]
    assert loc.search_keys("key_upper", NormalizeOptions(lower_case=False)) == []
    assert loc.search_values("acao") == ["  Ação  "]
    assert loc.search_values("  acao  ", NormalizeOptions(trim_spaces=False, normalize_letters=True)) == ["  Ação  "]
    assert loc.search_values("ação", NormalizeOptions(normalize_letters=False)) == ["  Ação  "]
    assert loc.search_values("nothing-matches") == []


def test_compare_ignores_unchanged_entries():
    old = localization()
    new = localization()

    diff = old.compare(new)

    assert diff.new_fields == [] and diff.edited_fields == [] and diff.deleted_fields == []

    with pytest.raises(LanguageMismatchError) as error:
        Localization.compare_between(old, Localization(ConfigLanguage.GERMAN, {}))

    assert "en != de" in str(error.value)


def test_translate_edge_cases():
    loc = localization()

    assert loc.translate([1, 2]) == [1, 2]
    assert loc.translate("text") == "text"

    translated = loc.translate(
        {
            "tid_name": "tid_unit_1_name",
            "type_name_key": "tid_attack_name_2",
            "tid_description": "tid_unit_1_description",
            "name_key": "tid_missing",
            "description_key": "tid_empty",
            "typeNameKey": 5,
        }
    )

    assert translated["name"] == "Dragon"
    assert translated["type_name"] == "Bite"
    assert translated["description"] == "A dragon"
    assert translated["name_key"] == "tid_missing"
    assert translated["description_key"] == "tid_empty"
    assert translated["typeNameKey"] == 5
    assert "tid_name" not in translated and "type_name_key" not in translated

    target = {"tid_name": "tid_unit_1_name"}
    loc.translate_object(target)
    assert target == {"name": "Dragon"}


async def test_default_client_is_created_and_closed(mock_http):
    mock_http(lambda request: httpx.Response(200, json=[{"a": "b"}]))

    assert await Localization.fetch(ConfigLanguage.ENGLISH) == [{"a": "b"}]
    assert (await Localization.create()).data == {"a": "b"}


async def test_default_client_errors_are_wrapped(mock_http):
    mock_http(lambda request: httpx.Response(503))

    with pytest.raises(LocalizationHttpError):
        await Localization.fetch()
