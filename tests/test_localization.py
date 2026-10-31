import httpx
import pytest

from dc_core import ConfigLanguage
from dc_localization import LanguageMismatchError, Localization, LocalizationHttpError, NormalizeOptions


def sample() -> Localization:
    return Localization(
        ConfigLanguage.ENGLISH,
        {
            "tid_unit_1000_name": "Nature Dragon",
            "tid_chest": "Chest",
            "tid_chest_type": "Épico",
        },
    )


def test_translates_known_keys_and_keeps_unknown_ones():
    source = {
        "id": 1,
        "chest_name_key": "tid_chest",
        "type_name_key": "tid_chest_type",
        "description_key": "tid_missing",
    }
    out = sample().translate(source)

    assert out["name"] == "Chest"
    assert out["type_name"] == "Épico"
    assert "chest_name_key" not in out
    assert out["description_key"] == "tid_missing"
    assert "chest_name_key" in source


def test_searches_ignore_case_and_accents():
    localization = sample()

    assert localization.search_values("epico") == ["Épico"]
    assert localization.search_values("epico", NormalizeOptions(normalize_letters=False)) == []
    assert localization.get_dragon_name(1000) == "Nature Dragon"
    assert localization.get_key_from_value("Chest") == "tid_chest"


def test_compare_detects_changes():
    old = sample()
    new = sample()
    new.data["tid_chest"] = "Big Chest"
    new.data["new"] = "x"
    del new.data["tid_unit_1000_name"]

    diff = old.compare(new)

    assert [field.key for field in diff.new_fields] == ["new"]
    assert [(f.key, f.values.old, f.values.new) for f in diff.edited_fields] == [("tid_chest", "Chest", "Big Chest")]
    assert [field.key for field in diff.deleted_fields] == ["tid_unit_1000_name"]

    with pytest.raises(LanguageMismatchError):
        old.compare(Localization(ConfigLanguage.FRENCH, {}))


async def test_create_merges_the_array_file():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("dc_android_pt_prod_wetd46pWuR8J5CmS.json")
        return httpx.Response(200, json=[{"a": "1"}, {"b": "2"}])

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        localization = await Localization.create(ConfigLanguage.PORTUGUESE, client)

    assert localization.data == {"a": "1", "b": "2"}
    assert localization.to_array() == [{"a": "1"}, {"b": "2"}]


async def test_http_errors_are_wrapped():
    transport = httpx.MockTransport(lambda request: httpx.Response(500))

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(LocalizationHttpError):
            await Localization.create(ConfigLanguage.ENGLISH, client)
