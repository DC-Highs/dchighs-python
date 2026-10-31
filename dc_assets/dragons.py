from typing import Optional, Union

from dc_assets.client import AssetDownloader
from dc_core import (
    DragonPhase,
    DragonSpriteQuality,
    SpriteQuality,
    StaticFileUrlPlatformPrefix,
    TextureCompressionFormat,
)

Phase = Union[DragonPhase, int]
Prefix = Union[StaticFileUrlPlatformPrefix, str]


def _base(platform_prefix: Prefix) -> str:
    return f"https://{platform_prefix}-static-s1.socialpointgames.com/static/dragoncity"


class _DragonDownloader(AssetDownloader):
    def __init__(
        self,
        image_name: str,
        phase: Phase,
        skin: Optional[str] = None,
        platform_prefix: Prefix = StaticFileUrlPlatformPrefix.IOS,
    ) -> None:
        self.image_name = image_name
        self.phase = int(phase)
        #: Skin suffix, e.g. ``"_1"``.
        self.skin = skin
        #: Static server prefix (defaults to iOS, ``dci``).
        self.platform_prefix = str(platform_prefix)

    @property
    def _name(self) -> str:
        return f"{self.image_name}{self.skin or ''}"


class DragonSpriteDownloader(_DragonDownloader):
    """Dragon sprite (``ui_<image><skin>_<phase><quality>.png``)."""

    def __init__(
        self,
        image_name: str,
        phase: Phase,
        skin: Optional[str] = None,
        image_quality: DragonSpriteQuality = SpriteQuality.NORMAL,
        platform_prefix: Prefix = StaticFileUrlPlatformPrefix.IOS,
    ) -> None:
        super().__init__(image_name, phase, skin, platform_prefix)
        self.image_quality = str(image_quality)

    @property
    def url(self) -> str:
        return (
            f"{_base(self.platform_prefix)}/mobile/ui/dragons/"
            f"ui_{self._name}_{self.phase}{self.image_quality}.png"
        )


class DragonThumbnailDownloader(_DragonDownloader):
    """Dragon thumbnail (``thumb_<image><skin>_<phase>.png``)."""

    @property
    def url(self) -> str:
        return f"{_base(self.platform_prefix)}/mobile/ui/dragons/HD/thumb_{self._name}_{self.phase}.png"


class DragonFlashAnimationDownloader(_DragonDownloader):
    """Flash animation (``.swf``)."""

    @property
    def url(self) -> str:
        return f"{_base(self.platform_prefix)}/assets/sprites/{self._name}_{self.phase}.swf"


class DragonSpineAnimationDownloader(_DragonDownloader):
    """Spine animation package (``.zip``).

    ``use_new_url_format=True`` (default) uses the ``_HD_tweened_`` package, ``False`` the legacy
    ``basic_..._spine-3-8-59`` one.
    """

    def __init__(
        self,
        image_name: str,
        phase: Phase,
        skin: Optional[str] = None,
        texture_compression_format: Union[TextureCompressionFormat, str] = TextureCompressionFormat.DXT5,
        platform_prefix: Prefix = StaticFileUrlPlatformPrefix.IOS,
        use_new_url_format: bool = True,
    ) -> None:
        super().__init__(image_name, phase, skin, platform_prefix)
        self.texture_compression_format = str(texture_compression_format)
        self.use_new_url_format = use_new_url_format

    @property
    def url(self) -> str:
        name = f"{self._name}_{self.phase}"
        directory = f"{_base(self.platform_prefix)}/mobile/engine/version_1_1/dragons/{name}"

        if self.use_new_url_format:
            return f"{directory}/{name}_HD_tweened_{self.texture_compression_format}.zip"

        return f"{directory}/basic_{name}_HD_spine-3-8-59_{self.texture_compression_format}.zip"
