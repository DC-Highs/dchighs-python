"""Buildings, decorations and habitats: sprites (``ui_<image><quality>.png``) and thumbnails (``<image>.jpg``)."""

from typing import Union

from dc_assets.client import AssetDownloader
from dc_core import SpriteQuality, StaticFileUrlPlatformPrefix

Prefix = Union[StaticFileUrlPlatformPrefix, str]


class _StructureSpriteDownloader(AssetDownloader):
    directory = ""

    def __init__(
        self,
        image_name: str,
        image_quality: SpriteQuality = SpriteQuality.NORMAL,
        platform_prefix: Prefix = StaticFileUrlPlatformPrefix.IOS,
    ) -> None:
        self.image_name = image_name
        self.image_quality = SpriteQuality(image_quality)
        self.platform_prefix = str(platform_prefix)

    @property
    def url(self) -> str:
        return (
            f"https://{self.platform_prefix}-static-s1.socialpointgames.com/static/dragoncity/mobile/ui/"
            f"{self.directory}/ui_{self.image_name}{self.image_quality}.png"
        )


class _StructureThumbnailDownloader(AssetDownloader):
    def __init__(
        self,
        image_name: str,
        platform_prefix: Prefix = StaticFileUrlPlatformPrefix.IOS,
    ) -> None:
        self.image_name = image_name
        self.platform_prefix = str(platform_prefix)

    @property
    def url(self) -> str:
        return (
            f"https://{self.platform_prefix}-static-s1.socialpointgames.com"
            f"/static/dragoncity/assets/thumbs/{self.image_name}.jpg"
        )


class BuildingSpriteDownloader(_StructureSpriteDownloader):
    """Building sprite."""

    directory = "buildings"


class DecorationSpriteDownloader(_StructureSpriteDownloader):
    """Decoration sprite."""

    directory = "decorations"


class HabitatSpriteDownloader(_StructureSpriteDownloader):
    """Habitat sprite."""

    directory = "habitats"


class BuildingThumbnailDownloader(_StructureThumbnailDownloader):
    """Building thumbnail (``.jpg``)."""


class DecorationThumbnailDownloader(_StructureThumbnailDownloader):
    """Decoration thumbnail (``.jpg``)."""


class HabitatThumbnailDownloader(_StructureThumbnailDownloader):
    """Habitat thumbnail (``.jpg``)."""
