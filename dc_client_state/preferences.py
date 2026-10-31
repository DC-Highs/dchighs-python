from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

from dc_client_state.user_default import UserDefault, UserDefaultEntry

_FARM_CROP_PREFIX = "retry_grow_type_food"


@dataclass(frozen=True)
class RetrySanctuaryDragons:
    left_account_dragon_id: int
    right_account_dragon_id: int


def _to_number(text: Optional[str]) -> Optional[float]:
    if not text:
        return None

    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return None


class Preferences:
    """High level API for the preferences stored in ``UserDefault.xml``."""

    def __init__(self, user_default: UserDefault) -> None:
        self.user_default = user_default

    def set_farm_crop_range(self, plant_id: int, start: int, end: int) -> None:
        """Plants ``plant_id`` on the crops numbered ``start`` (inclusive) to ``end`` (exclusive)."""
        entries = self.user_default.list_by_prefix(_FARM_CROP_PREFIX)
        self.user_default.set_many(
            (entry.key, plant_id) for counter, entry in enumerate(entries) if start <= counter < end
        )

    def set_all_farm_crops(self, plant_id: int) -> None:
        entries = self.user_default.list_by_prefix(_FARM_CROP_PREFIX)
        self.user_default.set_many((entry.key, plant_id) for entry in entries)

    def delete_all_farm_crops(self) -> None:
        entries = self.user_default.list_by_prefix(_FARM_CROP_PREFIX)
        self.user_default.delete_many(entry.key for entry in entries)

    def get_all_farm_crops(self) -> List[UserDefaultEntry]:
        return self.user_default.list_by_prefix(_FARM_CROP_PREFIX)

    def get_display_tutorials(self) -> List[UserDefaultEntry]:
        return self.user_default.list_by_include("tutorial")

    def set_display_tutorials(self, shown: bool) -> None:
        entries = self.user_default.list_by_include("tutorial")
        self.user_default.set_many((entry.key, shown) for entry in entries)

    def delete_display_tutorials(self) -> None:
        entries = self.user_default.list_by_include("tutorial")
        self.user_default.delete_many(entry.key for entry in entries)

    def disable_music(self) -> None:
        self.user_default.set("options_music_disabled", True)

    def enable_music(self) -> None:
        self.user_default.delete("options_music_disabled")

    def disable_sound(self) -> None:
        self.user_default.set("options_sound_disabled", True)

    def enable_sound(self) -> None:
        self.user_default.delete("options_sound_disabled")

    def get_user_id(self) -> Optional[int]:
        number = _to_number(self.user_default.get("user_origin_id"))
        return int(number) if number is not None else None

    def get_last_execution(self) -> Optional[datetime]:
        timestamp = _to_number(self.user_default.get("last_execution"))

        if timestamp is None:
            return None

        return datetime.fromtimestamp(timestamp, tz=timezone.utc)

    def get_retry_breed_sanctuary_dragons(self) -> Optional[RetrySanctuaryDragons]:
        left = self.user_default.list_by_include("left_retry_breeed_dragon")
        right = self.user_default.list_by_include("right_retry_breeed_dragon")

        if not left or not right:
            return None

        left_id, right_id = _to_number(left[0].text), _to_number(right[0].text)

        if left_id is None or right_id is None:
            return None

        return RetrySanctuaryDragons(int(left_id), int(right_id))

    def set_retry_breed_sanctuary_dragons(self, left_account_dragon_id: int, right_account_dragon_id: int) -> None:
        self.user_default.set_many(
            [
                ("left_retry_breeed_dragon_444", left_account_dragon_id),
                ("right_retry_breeed_dragon_444", right_account_dragon_id),
            ]
        )
