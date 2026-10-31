from datetime import datetime, timezone

import pytest

from dc_client_state import (
    AssetType,
    Assets,
    ClientState,
    ClientStateError,
    Preferences,
    UserDefault,
)

XML = """<?xml version="1.0" encoding="utf-8"?>
<userDefaultRoot>
    <entry key="user_origin_id">12345</entry>
    <entry key="last_execution">1700000000</entry>
    <entry key="retry_grow_type_food_1">1</entry>
    <entry key="retry_grow_type_food_2">1</entry>
    <entry key="retry_grow_type_food_3">1</entry>
    <entry key="tutorial_intro">true</entry>
    <entry key="left_retry_breeed_dragon_9">100</entry>
    <entry key="right_retry_breeed_dragon_9">200</entry>
</userDefaultRoot>
"""


@pytest.fixture
def user_default(tmp_path):
    path = tmp_path / "UserDefault.xml"
    path.write_text(XML, encoding="utf-8")
    return UserDefault(path)


def test_get_set_delete(user_default):
    assert user_default.get("user_origin_id") == "12345"
    assert user_default.get("missing") is None

    user_default.set("user_origin_id", "999")
    user_default.set("flag", True)
    user_default.set("object", {"a": 1})
    user_default.set("number", 12)
    user_default.delete("last_execution")

    assert user_default.get("user_origin_id") == "999"
    assert user_default.get("flag") == "true"
    assert user_default.get("object") == '{"a":1}'
    assert user_default.get("number") == "12"
    assert user_default.get("last_execution") is None
    assert user_default.file_path.read_text(encoding="utf-8").startswith('<?xml version="1.0" encoding="utf-8"?>')


def test_single_entry_files_work(tmp_path):
    path = tmp_path / "UserDefault.xml"
    path.write_text('<userDefaultRoot><entry key="only">1</entry></userDefaultRoot>', encoding="utf-8")
    user_default = UserDefault(path)

    assert [entry.key for entry in user_default.get_entries()] == ["only"]
    user_default.set("second", 2)
    assert user_default.get("second") == "2"


def test_list_helpers(user_default):
    assert [e.key for e in user_default.list_by_prefix("retry_grow")] == [
        "retry_grow_type_food_1", "retry_grow_type_food_2", "retry_grow_type_food_3",
    ]
    assert [e.key for e in user_default.list_by_include("tutorial")] == ["tutorial_intro"]


def test_preferences(user_default):
    preferences = Preferences(user_default)

    assert preferences.get_user_id() == 12345
    assert preferences.get_last_execution() == datetime(2023, 11, 14, 22, 13, 20, tzinfo=timezone.utc)

    preferences.set_farm_crop_range(plant_id=7, start=1, end=3)
    assert [e.text for e in preferences.get_all_farm_crops()] == ["1", "7", "7"]

    preferences.set_all_farm_crops(5)
    assert {e.text for e in preferences.get_all_farm_crops()} == {"5"}

    preferences.delete_all_farm_crops()
    assert preferences.get_all_farm_crops() == []

    preferences.set_display_tutorials(False)
    assert preferences.get_display_tutorials()[0].text == "false"
    preferences.delete_display_tutorials()
    assert preferences.get_display_tutorials() == []

    preferences.disable_music()
    preferences.disable_sound()
    assert user_default.get("options_music_disabled") == "true"
    preferences.enable_music()
    preferences.enable_sound()
    assert user_default.get("options_music_disabled") is None
    assert user_default.get("options_sound_disabled") is None

    dragons = preferences.get_retry_breed_sanctuary_dragons()
    assert (dragons.left_account_dragon_id, dragons.right_account_dragon_id) == (100, 200)

    preferences.set_retry_breed_sanctuary_dragons(1, 2)
    assert user_default.get("left_retry_breeed_dragon_444") == "1"


def test_preferences_without_data(tmp_path):
    path = tmp_path / "UserDefault.xml"
    path.write_text("<userDefaultRoot></userDefaultRoot>", encoding="utf-8")
    preferences = Preferences(UserDefault(path))

    assert preferences.get_user_id() is None
    assert preferences.get_last_execution() is None
    assert preferences.get_retry_breed_sanctuary_dragons() is None


def test_assets(tmp_path):
    directory = tmp_path / "assets"
    directory.mkdir()
    (directory / "a.png").write_bytes(b"1")
    (directory / "b.mp3").write_bytes(b"2")
    (directory / "c.dds").write_bytes(b"3")
    replacement = tmp_path / "new.png"
    replacement.write_bytes(b"new")

    assets = Assets(directory)

    assert [p.name for p in assets.list_assets()] == ["a.png", "b.mp3", "c.dds"]
    assert [p.name for p in assets.list_assets([AssetType.IMAGE, AssetType.TEXTURE])] == ["a.png", "c.dds"]

    assets.set("a.png", replacement)
    assert assets.get_file_path("a.png").read_bytes() == b"new"

    assets.delete("b.mp3")
    assert [p.name for p in assets.list_assets()] == ["a.png", "c.dds"]

    assets.clear_assets()
    assert assets.list_assets() == []


def test_client_state_finds_the_dragon_city_package(tmp_path):
    (tmp_path / "Other.App_1").mkdir()
    (tmp_path / "SocialPoint.DragonCityMobile_abc").mkdir()

    state = ClientState(packages_dir_path=tmp_path)

    assert state.dragon_city_dir_name == "SocialPoint.DragonCityMobile_abc"
    assert state.assets_dir_path == (
        tmp_path / "SocialPoint.DragonCityMobile_abc" / "LocalCache" / "Local" / "Social Point" / "DragonCity"
    )
    assert state.user_default.file_path.name == "UserDefault.xml"


def test_client_state_errors(tmp_path):
    with pytest.raises(ClientStateError):
        ClientState(packages_dir_path=tmp_path)

    with pytest.raises(ClientStateError):
        ClientState.find_dragon_city_dir_name(tmp_path / "does-not-exist")
