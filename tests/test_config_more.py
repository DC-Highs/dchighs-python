import httpx
import pytest

from dc_config import Config, ConfigFilter, ConfigHttpError, CreateOptions, FetchOptions, FetchRawOptions, GameConfig


async def test_default_client_is_created_for_each_request(mock_http):
    mock_http(lambda request: httpx.Response(200, json={"game_data": {"config": {"items": []}}}))

    assert list((await Config.fetch(FetchOptions("https://x", "1", "t"))).config.keys()) == ["items"]
    assert (await Config.fetch_raw(FetchRawOptions("https://x"))).config.section(ConfigFilter.ITEMS) == []
    assert isinstance(CreateOptions("https://x", "1", "t"), FetchOptions)


async def test_invalid_json_is_a_config_error(mock_http):
    mock_http(lambda request: httpx.Response(200, content=b"not json"))

    with pytest.raises(ConfigHttpError):
        await Config.fetch_raw(FetchRawOptions("https://x"))


def test_malformed_documents_are_rejected():
    with pytest.raises(ValueError):
        GameConfig.from_dict({"game_data": {"config": []}})

    with pytest.raises(ValueError):
        GameConfig.from_dict({"game_data": 3})
