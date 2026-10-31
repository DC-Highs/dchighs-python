from typing import Union

from dc_assets.client import AssetDownloader
from dc_core import StaticFileUrlPlatformPrefix


class MusicDownloader(AssetDownloader):
    """Music track (``.mp3``)."""

    def __init__(
        self,
        key_name: str,
        platform_prefix: Union[StaticFileUrlPlatformPrefix, str] = StaticFileUrlPlatformPrefix.IOS,
    ) -> None:
        self.key_name = key_name
        #: Static server prefix (defaults to iOS, ``dci``).
        self.platform_prefix = str(platform_prefix)

    @property
    def url(self) -> str:
        # The original server path is plain HTTP; kept as is.
        return (
            f"http://{self.platform_prefix}-static-s1.socialpointgames.com"
            f"/static/dragoncity/mobile/sounds/music/{self.key_name}.mp3"
        )
