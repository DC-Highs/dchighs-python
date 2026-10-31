import pytest

from dc_client_state import (
    AssetType,
    Assets,
    ClientState,
    ClientStateError,
    ClientStateOptions,
    Preferences,
    UserDefault,
    default_packages_dir,
)

XML = """<?xml version='1.0' encoding='utf-16'?>
<userDefaultRoot>
    <entry key="user_origin_id">abc</entry>
    <entry key="last_execution">1.5</entry>
    <entry key="left_retry_breeed_dragon_1">x</entry>
    <entry key="right_retry_breeed_dragon_1">2</entry>
    <entry key="empty"/>
</userDefaultRoot>
""".replace("utf-16", "utf-8")


@pytest.fixture
def user_default(tmp_path):
    path = tmp_path / "UserDefault.xml"
    path.write_text(XML, encoding="utf-8")
    return UserDefault(path)


def test_default_packages_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert default_packages_dir() == tmp_path / "Packages"

    monkeypatch.delenv("LOCALAPPDATA")
    assert default_packages_dir() is None

    with pytest.raises(ClientStateError):
        ClientState()

    with pytest.raises(ClientStateError):
        ClientState.find_dragon_city_dir_name()


def test_client_state_from_options(tmp_path):
    (tmp_path / "SocialPoint.DragonCityMobile_x").mkdir()
    (tmp_path / "SocialPoint.DragonCityMobile_y").mkdir()

    default = ClientState.from_options(ClientStateOptions(packages_dir_path=tmp_path))
    explicit = ClientState.from_options(
        ClientStateOptions(packages_dir_path=tmp_path, dragon_city_dir_name="SocialPoint.DragonCityMobile_y")
    )

    assert default.dragon_city_dir_name == "SocialPoint.DragonCityMobile_x"
    assert explicit.dragon_city_dir_name == "SocialPoint.DragonCityMobile_y"


def test_user_default_helpers(user_default):
    assert user_default.read_raw().getroot().tag == "userDefaultRoot"
    assert user_default.get("empty") is None

    user_default.update_where(lambda key: key.startswith("left"), "changed")
    assert user_default.get("left_retry_breeed_dragon_1") == "changed"
    assert user_default.get("right_retry_breeed_dragon_1") == "2"


def test_xml_declaration_is_optional_and_normalized(tmp_path):
    path = tmp_path / "plain.xml"
    path.write_text("<userDefaultRoot><entry key='a'>1</entry></userDefaultRoot>", encoding="utf-8")
    plain = UserDefault(path)
    plain.set("b", "2")
    assert not path.read_text(encoding="utf-8").startswith("<?xml")

    declared = tmp_path / "declared.xml"
    declared.write_text(
        "<?xml version='1.0' encoding='ISO-8859-1'?><userDefaultRoot/>", encoding="latin-1"
    )
    UserDefault(declared).set("c", "ç")
    assert 'encoding="utf-8"' in declared.read_text(encoding="utf-8")


def test_preferences_with_malformed_values(user_default):
    preferences = Preferences(user_default)

    assert preferences.get_user_id() is None
    assert preferences.get_last_execution().timestamp() == 1.5
    assert preferences.get_retry_breed_sanctuary_dragons() is None

    user_default.set("user_origin_id", "7.0")
    assert preferences.get_user_id() == 7


def test_asset_listing_and_clearing_ignore_directories(tmp_path):
    (tmp_path / "folder").mkdir()
    (tmp_path / "a.png").write_bytes(b"1")
    assets = Assets(tmp_path)

    assert [p.name for p in assets.list_assets([AssetType.MASK, AssetType.BINARY])] == []
    assert str(AssetType.IMAGE) == "image"

    assets.clear_assets()

    assert [p.name for p in assets.list_assets()] == ["folder"]
