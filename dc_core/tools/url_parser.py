import re
from dataclasses import dataclass
from typing import Optional

from dc_core.enums import DragonPhase, DragonSpriteQuality, StaticFileUrlPlatformPrefix

_PREFIX_RE = re.compile(r"https?://([a-z]+)-static", re.IGNORECASE)
_IMAGE_RE = re.compile(r"/(?:basic_|thumb_|ui_)?(\d+)_([\w_]+)")
_ID_RE = re.compile(r"/(?:basic_|thumb_|ui_)?(\d+)_")
_PHASE_RE = re.compile(
    r"(\d+)@2x\.(?:png|swf)|(\d+)\.(?:png|swf)|(\d+)_HD_tweened_dxt5\.zip|(\d+)_HD_spine-3-8-59_dxt5\.zip"
)
_SKIN_RE = re.compile(r"_skin\d+")
_QUALITY_RE = re.compile(r"@\d+x")
_DIGITS_UNDERSCORE_RE = re.compile(r"_\d+")


@dataclass
class DragonParsedSprite:
    platform_prefix: Optional[StaticFileUrlPlatformPrefix]
    id: Optional[int]
    image_name: Optional[str]
    phase: Optional[DragonPhase]
    skin: Optional[str]
    image_quality: DragonSpriteQuality


@dataclass
class DragonParsedThumbnail:
    platform_prefix: Optional[StaticFileUrlPlatformPrefix]
    id: Optional[int]
    image_name: Optional[str]
    phase: Optional[DragonPhase]
    skin: Optional[str]


class DragonStaticFileUrlParser:
    """Extracts the dragon information embedded in the URLs of the static servers."""

    @staticmethod
    def get_platform_prefix(url: str) -> Optional[StaticFileUrlPlatformPrefix]:
        match = _PREFIX_RE.search(url)

        if match is None:
            return None

        try:
            return StaticFileUrlPlatformPrefix(match.group(1).lower())
        except ValueError:
            return None

    @staticmethod
    def get_image_name(url: str) -> Optional[str]:
        match = _IMAGE_RE.search(url)

        if match is None:
            return None

        raw = f"{match.group(1)}_{match.group(2)}"
        without_digits = _DIGITS_UNDERSCORE_RE.sub("", raw, count=1)
        return _SKIN_RE.sub("", without_digits, count=1)

    @staticmethod
    def get_id(url: str) -> Optional[int]:
        match = _ID_RE.search(url)
        return int(match.group(1)) if match is not None else None

    @staticmethod
    def get_phase(url: str) -> Optional[DragonPhase]:
        match = _PHASE_RE.search(url)

        if match is None:
            return None

        phase = next((group for group in match.groups() if group is not None), None)

        if phase is None:
            return None

        try:
            return DragonPhase(int(phase))
        except ValueError:
            return None

    @staticmethod
    def get_skin(url: str) -> Optional[str]:
        match = _SKIN_RE.search(url)
        return match.group(0) if match is not None else None

    @staticmethod
    def get_image_quality(url: str) -> DragonSpriteQuality:
        if _QUALITY_RE.search(url):
            return DragonSpriteQuality.LARGE

        return DragonSpriteQuality.NORMAL

    @classmethod
    def parse_from_sprite(cls, url: str) -> DragonParsedSprite:
        return DragonParsedSprite(
            platform_prefix=cls.get_platform_prefix(url),
            id=cls.get_id(url),
            image_name=cls.get_image_name(url),
            phase=cls.get_phase(url),
            skin=cls.get_skin(url),
            image_quality=cls.get_image_quality(url),
        )

    @classmethod
    def parse_from_thumbnail(cls, url: str) -> DragonParsedThumbnail:
        return DragonParsedThumbnail(
            platform_prefix=cls.get_platform_prefix(url),
            id=cls.get_id(url),
            image_name=cls.get_image_name(url),
            phase=cls.get_phase(url),
            skin=cls.get_skin(url),
        )

    @classmethod
    def parse_from_flash_animation(cls, url: str) -> DragonParsedThumbnail:
        return cls.parse_from_thumbnail(url)

    @classmethod
    def parse_from_spine_animation(cls, url: str) -> DragonParsedThumbnail:
        return cls.parse_from_thumbnail(url)
