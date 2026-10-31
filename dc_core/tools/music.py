from typing import Optional

from dc_core.settings.sounds import MUSIC_KEY_NAMES


def get_music_name_from_tag(tag: str) -> Optional[str]:
    """Resolves the music key name of an island ``sound_tag``."""
    tag_lower = tag.lower()
    music_name_1 = f"dc_{tag_lower}_island"
    music_name_2 = f"_{tag_lower}"

    for name in MUSIC_KEY_NAMES:
        if music_name_1 in name or name.endswith(music_name_2):
            return name

    return None
