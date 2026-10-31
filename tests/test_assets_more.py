import httpx
import pytest

from dc_assets import (
    AssetDownloader,
    AssetsError,
    InvalidArgumentsError,
    MusicDownloader,
    fetch_first,
)


async def test_fetch_first_needs_at_least_one_url():
    with pytest.raises(InvalidArgumentsError):
        await fetch_first([])


async def test_default_client_is_created_and_used(mock_http):
    mock_http(lambda request: httpx.Response(200, content=b"mp3"))

    assert await MusicDownloader("a").fetch() == b"mp3"


async def test_download_reports_disk_errors(mock_http, tmp_path):
    mock_http(lambda request: httpx.Response(200, content=b"data"))

    with pytest.raises(AssetsError):
        await MusicDownloader("a").download(tmp_path)


def test_abstract_downloader_has_no_url():
    with pytest.raises(NotImplementedError):
        AssetDownloader().url
