from typing import List, Union

from dc_assets.client import AssetDownloader
from dc_assets.errors import InvalidArgumentsError
from dc_core import IslandType, SpriteQuality


class IslandPackageDownloader(AssetDownloader):
    """Island content package (``.zip``).

    ``island_type`` is an :class:`~dc_core.IslandType` (e.g. ``IslandType.HEROIC_RACES``) or its
    string value, ``file_name`` the package file name.
    """

    def __init__(self, island_type: Union[IslandType, str], file_name: str) -> None:
        island_type = str(island_type)

        if island_type == IslandType.GRID_ISLANDS.value and not file_name.endswith("_optim.zip"):
            file_name = file_name.replace(".zip", "_optim.zip", 1)

        directory = "heroicraces_islands" if island_type == IslandType.HEROIC_RACES.value else island_type

        self.island_type = island_type
        self.file_name = file_name
        self._url = (
            f"https://www.socialpointgames.com/static/dragoncity/mobile/ui/{directory}/HD/dxt5/{file_name}"
        )

    @classmethod
    def from_path(cls, path: str) -> "IslandPackageDownloader":
        """From a configuration ``zip_file`` path such as
        ``/static/dragoncity/mobile/<island_type>/<file>.zip`` (island type is the 4th and
        file name the 5th ``/``-separated segment)."""
        segments = path.split("/")

        if len(segments) >= 5 and segments[3] and segments[4]:
            return cls(segments[3], segments[4])

        raise InvalidArgumentsError(f"cannot extract island type and file name from path {path!r}")

    @property
    def url(self) -> str:
        return self._url


class ChestSpriteDownloader(AssetDownloader):
    """Chest sprite. Tries ``ui_<image><quality>.png`` first and falls back to
    ``ui_basic_<image><quality>.png``."""

    _BASE = "https://dci-static-s1.socialpointgames.com/static/dragoncity/mobile/ui/chests"

    def __init__(self, image_name: str, image_quality: SpriteQuality = SpriteQuality.NORMAL) -> None:
        self.image_name = image_name
        self.image_quality = SpriteQuality(image_quality)

    @property
    def url(self) -> str:
        return f"{self._BASE}/ui_{self.image_name}{self.image_quality}.png"

    @property
    def basic_url(self) -> str:
        """The fallback URL used when the main one is not available."""
        return f"{self._BASE}/ui_basic_{self.image_name}{self.image_quality}.png"

    @property
    def urls(self) -> List[str]:
        return [self.url, self.basic_url]
