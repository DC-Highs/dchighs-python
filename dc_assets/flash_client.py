from typing import Union

from dc_assets.client import AssetDownloader
from dc_core import StaticFileUrlPlatformPrefix


class FlashClientDownloader(AssetDownloader):
    """A version of the Dragon City Flash client (``Base_sec_<version>.swf``), e.g. ``"2.2.5"``."""

    def __init__(
        self,
        version: str,
        platform_prefix: Union[StaticFileUrlPlatformPrefix, str] = StaticFileUrlPlatformPrefix.IOS,
    ) -> None:
        self.version = version
        #: Static server prefix (defaults to iOS, ``dci``).
        self.platform_prefix = str(platform_prefix)

    @property
    def url(self) -> str:
        return (
            f"https://{self.platform_prefix}-static-s1.socialpointgames.com"
            f"/static/dragoncity/flash/Base_sec_{self.version}.swf"
        )
