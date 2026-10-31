import httpx
import pytest

from dc_assets import (
    AssetsHttpError,
    BuildingSpriteDownloader,
    BuildingThumbnailDownloader,
    ChestSpriteDownloader,
    DecorationSpriteDownloader,
    DragonFlashAnimationDownloader,
    DragonSpineAnimationDownloader,
    DragonSpriteDownloader,
    DragonThumbnailDownloader,
    HabitatSpriteDownloader,
    InvalidArgumentsError,
    IslandPackageDownloader,
    IslandType,
    MusicDownloader,
)
from dc_core import DragonPhase, SpriteQuality


def test_sprite_url_matches_the_typescript_package():
    sprite = DragonSpriteDownloader(
        "1000_dragon_nature", DragonPhase.ADULT, skin="_1", image_quality=SpriteQuality.LARGE
    )

    assert sprite.url == (
        "https://dci-static-s1.socialpointgames.com/static/dragoncity/mobile/ui/dragons/"
        "ui_1000_dragon_nature_1_3@2x.png"
    )


def test_spine_urls():
    new = DragonSpineAnimationDownloader("1000_dragon_nature", DragonPhase.BABY)
    assert new.url.endswith("1000_dragon_nature_1/1000_dragon_nature_1_HD_tweened_dxt5.zip")

    old = DragonSpineAnimationDownloader(
        "1000_dragon_nature", DragonPhase.BABY, platform_prefix="dca", use_new_url_format=False
    )
    assert old.url.startswith("https://dca-static-s1.")
    assert old.url.endswith("basic_1000_dragon_nature_1_HD_spine-3-8-59_dxt5.zip")


def test_thumbnail_and_flash_urls():
    assert DragonThumbnailDownloader("a", DragonPhase.EGG).url.endswith("/mobile/ui/dragons/HD/thumb_a_0.png")
    assert DragonFlashAnimationDownloader("a", 2).url.endswith("/assets/sprites/a_2.swf")


def test_island_package_urls():
    assert IslandPackageDownloader(IslandType.HEROIC_RACES, "a.zip").url == (
        "https://www.socialpointgames.com/static/dragoncity/mobile/ui/heroicraces_islands/HD/dxt5/a.zip"
    )
    assert IslandPackageDownloader("grid_islands", "a.zip").url.endswith("/a_optim.zip")
    assert IslandPackageDownloader("grid_islands", "a_optim.zip").url.endswith("/a_optim.zip")
    assert "/maze_islands/" in IslandPackageDownloader("maze_islands", "a.zip").url


def test_island_package_from_path():
    downloader = IslandPackageDownloader.from_path("/static/dragoncity/maze_islands/file.zip")
    assert downloader.url.endswith("/maze_islands/HD/dxt5/file.zip")

    with pytest.raises(InvalidArgumentsError):
        IslandPackageDownloader.from_path("short")


def test_chest_has_a_fallback():
    chest = ChestSpriteDownloader("abc", SpriteQuality.LARGE)

    assert chest.url.endswith("/chests/ui_abc@2x.png")
    assert chest.basic_url.endswith("/chests/ui_basic_abc@2x.png")
    assert len(chest.urls) == 2


def test_building_decoration_and_habitat_urls():
    sprite = BuildingSpriteDownloader(
        "10552_hatchery6reskinart_building", SpriteQuality.LARGE, platform_prefix="dca"
    )
    assert sprite.url == (
        "https://dca-static-s1.socialpointgames.com/static/dragoncity/mobile/ui/buildings/"
        "ui_10552_hatchery6reskinart_building@2x.png"
    )
    assert BuildingThumbnailDownloader("x").url == (
        "https://dci-static-s1.socialpointgames.com/static/dragoncity/assets/thumbs/x.jpg"
    )
    assert "/ui/decorations/ui_x.png" in DecorationSpriteDownloader("x").url
    assert "/ui/habitats/ui_x.png" in HabitatSpriteDownloader("x").url


def test_music_url():
    assert MusicDownloader("531_dc_party_planning_island").url == (
        "http://dci-static-s1.socialpointgames.com/static/dragoncity/mobile/sounds/music/"
        "531_dc_party_planning_island.mp3"
    )


async def test_fetch_falls_back_to_the_next_url_and_download_writes_the_file(tmp_path):
    requested = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested.append(request.url.path)
        return httpx.Response(404) if "ui_basic_" not in request.url.path else httpx.Response(200, content=b"png")

    chest = ChestSpriteDownloader("abc")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        assert await chest.fetch(client) == b"png"
        target = await chest.download(tmp_path / "chest.png", client)

    assert target.read_bytes() == b"png"
    assert requested[:2] == [
        "/static/dragoncity/mobile/ui/chests/ui_abc.png",
        "/static/dragoncity/mobile/ui/chests/ui_basic_abc.png",
    ]


async def test_fetch_reports_http_errors():
    transport = httpx.MockTransport(lambda request: httpx.Response(404))

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(AssetsHttpError):
            await MusicDownloader("x").fetch(client)
