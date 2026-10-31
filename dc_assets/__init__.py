"""Download static assets (sprites, thumbnails, animations, music) from the Dragon City servers.

Every downloader is a small object that knows its URL. It can either save the file to disk with
``await downloader.download(path)`` or give you the bytes with ``await downloader.fetch()``.

.. code-block:: python

    from dc_assets import DragonSpriteDownloader
    from dc_core import DragonPhase, SpriteQuality

    sprite = DragonSpriteDownloader("1000_dragon_nature", DragonPhase.ADULT, image_quality=SpriteQuality.LARGE)
    await sprite.download("dragon-sprite.png")

Fan-made library, not affiliated with SocialPoint.
"""

from dc_assets.client import AssetDownloader, fetch_first
from dc_assets.dragons import (
    DragonFlashAnimationDownloader,
    DragonSpineAnimationDownloader,
    DragonSpriteDownloader,
    DragonThumbnailDownloader,
)
from dc_assets.flash_client import FlashClientDownloader
from dc_assets.errors import AssetsError, AssetsHttpError, InvalidArgumentsError
from dc_assets.islands import ChestSpriteDownloader, IslandPackageDownloader
from dc_assets.sounds import MusicDownloader
from dc_assets.structures import (
    BuildingSpriteDownloader,
    BuildingThumbnailDownloader,
    DecorationSpriteDownloader,
    DecorationThumbnailDownloader,
    HabitatSpriteDownloader,
    HabitatThumbnailDownloader,
)
from dc_core import (
    BuildingSpriteQuality,
    ChestSpriteQuality,
    DecorationSpriteQuality,
    DragonPhase,
    DragonSpriteQuality,
    HabitatSpriteQuality,
    IslandType,
    SpriteQuality,
    StaticFileUrlPlatformPrefix,
    TextureCompressionFormat,
)

__all__ = [
    "AssetDownloader",
    "AssetsError",
    "AssetsHttpError",
    "BuildingSpriteDownloader",
    "BuildingSpriteQuality",
    "BuildingThumbnailDownloader",
    "ChestSpriteDownloader",
    "ChestSpriteQuality",
    "DecorationSpriteDownloader",
    "DecorationSpriteQuality",
    "DecorationThumbnailDownloader",
    "DragonFlashAnimationDownloader",
    "DragonPhase",
    "DragonSpineAnimationDownloader",
    "DragonSpriteDownloader",
    "DragonSpriteQuality",
    "DragonThumbnailDownloader",
    "FlashClientDownloader",
    "HabitatSpriteDownloader",
    "HabitatSpriteQuality",
    "HabitatThumbnailDownloader",
    "InvalidArgumentsError",
    "IslandPackageDownloader",
    "IslandType",
    "MusicDownloader",
    "SpriteQuality",
    "StaticFileUrlPlatformPrefix",
    "TextureCompressionFormat",
    "fetch_first",
]
