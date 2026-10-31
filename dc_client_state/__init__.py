"""Dragon City client state manager for Windows 10 or Windows 11.

Python port of ``@dchighs/dc-client-state``: edit the preferences (``UserDefault.xml``) and the cached
assets of the Dragon City client installed from the Microsoft Store.

Fan-made library, not affiliated with SocialPoint.
"""

from dc_client_state.assets import EXTENSION_MAP, Assets
from dc_client_state.client_state import (
    ClientState,
    ClientStateError,
    ClientStateOptions,
    default_packages_dir,
)
from dc_client_state.enums import AssetType
from dc_client_state.preferences import Preferences, RetrySanctuaryDragons
from dc_client_state.user_default import UserDefault, UserDefaultEntry

__all__ = [
    "AssetType",
    "Assets",
    "ClientState",
    "ClientStateError",
    "ClientStateOptions",
    "EXTENSION_MAP",
    "Preferences",
    "RetrySanctuaryDragons",
    "UserDefault",
    "UserDefaultEntry",
    "default_packages_dir",
]
