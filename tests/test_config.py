import httpx
import pytest

from dc_config import (
    Config,
    ConfigFilter,
    ConfigHttpError,
    ConfigLanguage,
    ConfigPlatform,
    CreateRawOptions,
    FetchOptions,
    FetchRawOptions,
    GameConfig,
    filter_config,
)


def sample() -> GameConfig:
    return GameConfig.from_dict(
        {"game_data": {"config": {"items": [1], "chests": {"a": 1}, "levels": []}}}
    )


def test_filter_keeps_only_requested_present_sections():
    filtered = filter_config(sample(), [ConfigFilter.ITEMS, ConfigFilter.SKILLS])
    assert list(filtered.config.keys()) == ["items"]


def test_empty_filter_keeps_everything():
    assert len(list(filter_config(sample(), None).config.keys())) == 3
    assert len(list(filter_config(sample(), []).config.keys())) == 3


def test_typed_access():
    config = sample().config

    assert config.get(ConfigFilter.ITEMS, list) == [1]
    assert config.section("chests") == {"a": 1}
    assert config.get(ConfigFilter.SKILLS) is None
    assert ConfigFilter.ITEMS in config

    with pytest.raises(Exception):
        config.get(ConfigFilter.CHESTS, list)


def test_repr_hides_the_auth_token():
    options = FetchOptions("https://x", "1", "secret-token")
    assert "secret-token" not in repr(options)


def test_json_roundtrip(tmp_path):
    path = tmp_path / "config.json"
    path.write_text('{"game_data": {"config": {"items": []}}}', encoding="utf-8")

    assert GameConfig.from_file(path).to_dict() == {"game_data": {"config": {"items": []}}}

    with pytest.raises(ValueError):
        GameConfig.from_json_str("{}")


async def test_create_posts_to_the_authenticated_endpoint():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["params"] = dict(request.url.params)
        return httpx.Response(200, json={"game_data": {"config": {"items": [1]}}})

    options = FetchOptions(
        "https://example.com/config",
        "42",
        "token",
        language=ConfigLanguage.TURKISH,
        platform=ConfigPlatform.ANDROID,
        filter=[ConfigFilter.ITEMS, ConfigFilter.CHESTS],
    )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        config = await Config.create(options, client)

    assert seen["method"] == "POST"
    assert seen["params"] == {
        "authToken": "token",
        "userId": "42",
        "filter": "items,chests",
        "platform": "android",
        "language": "tr",
    }
    assert config.language is ConfigLanguage.TURKISH
    assert config.platform is ConfigPlatform.ANDROID
    assert config.data.config.section(ConfigFilter.ITEMS) == [1]


async def test_create_raw_filters_the_sections():
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200, json={"game_data": {"config": {"items": [1], "chests": {}, "levels": []}}}
        )
    )

    async with httpx.AsyncClient(transport=transport) as client:
        config = await Config.create_raw(CreateRawOptions("https://x", filter=[ConfigFilter.LEVELS]), client)
        everything = await Config.fetch_raw(FetchRawOptions("https://x"), client)

    assert list(config.data.config.keys()) == ["levels"]
    assert config.language is ConfigLanguage.ENGLISH and config.platform is ConfigPlatform.IOS
    assert len(everything.config) == 3


async def test_http_errors_are_wrapped():
    transport = httpx.MockTransport(lambda request: httpx.Response(403))

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(ConfigHttpError):
            await Config.fetch(FetchOptions("https://x", "1", "t"), client)
