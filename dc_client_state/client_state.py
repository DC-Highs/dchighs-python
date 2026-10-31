import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from dc_client_state.assets import Assets
from dc_client_state.preferences import Preferences
from dc_client_state.user_default import UserDefault

_DRAGON_CITY_DIR_PREFIX = "SocialPoint.DragonCityMobile_"


class ClientStateError(Exception):
    """The Dragon City client state could not be located."""


def default_packages_dir() -> Optional[Path]:
    """``%LOCALAPPDATA%\\Packages`` (Windows), ``None`` when ``LOCALAPPDATA`` is not set."""
    local_app_data = os.environ.get("LOCALAPPDATA")
    return Path(local_app_data) / "Packages" if local_app_data else None


def _ensure_packages_dir(packages_dir_path: Union[str, Path, None]) -> Path:
    final = Path(packages_dir_path) if packages_dir_path else default_packages_dir()

    if final is None:
        raise ClientStateError("Unable to find packages directory")

    return final


@dataclass
class ClientStateOptions:
    packages_dir_path: Optional[Union[str, Path]] = None
    dragon_city_dir_name: Optional[str] = None


class ClientState:
    """The state of the Dragon City client installed from the Microsoft Store (Windows 10/11):
    its preferences (:attr:`user_default`, :attr:`preferences`) and cached assets (:attr:`assets`)."""

    def __init__(
        self,
        packages_dir_path: Union[str, Path, None] = None,
        dragon_city_dir_name: Optional[str] = None,
    ) -> None:
        self.packages_dir_path = _ensure_packages_dir(packages_dir_path)
        self.dragon_city_dir_name = dragon_city_dir_name or self.find_dragon_city_dir_name(self.packages_dir_path)
        self.dragon_city_dir_path = self.packages_dir_path / self.dragon_city_dir_name
        self.assets_dir_path = self.dragon_city_dir_path / "LocalCache" / "Local" / "Social Point" / "DragonCity"
        self.user_default_file_path = (
            self.dragon_city_dir_path / "LocalCache" / "Local" / "DragonCity" / "UserDefault.xml"
        )

        self.user_default = UserDefault(self.user_default_file_path)
        self.preferences = Preferences(self.user_default)
        self.assets = Assets(self.assets_dir_path)

    @classmethod
    def from_options(cls, options: ClientStateOptions) -> "ClientState":
        return cls(options.packages_dir_path, options.dragon_city_dir_name)

    @staticmethod
    def find_dragon_city_dir_name(packages_dir_path: Union[str, Path, None] = None) -> str:
        packages = _ensure_packages_dir(packages_dir_path)

        try:
            names = sorted(path.name for path in packages.iterdir())
        except OSError as error:
            raise ClientStateError(f"Unable to read the packages directory: {error}") from error

        for name in names:
            if name.startswith(_DRAGON_CITY_DIR_PREFIX):
                return name

        raise ClientStateError("Unable to find Dragon City directory")
