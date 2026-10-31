# dc_client_state

Manage the state of the Dragon City client installed from the Microsoft Store on Windows 10/11: its preferences
(`UserDefault.xml`) and cached assets. Port of `@dchighs/dc-client-state` — **not** part of the Rust ports.

Extra: `client-state` (no third-party dependencies; XML through the standard library). Everything here is
synchronous file I/O. Close the game before editing its files.

## `ClientState`

```python
from dc_client_state import ClientState

state = ClientState()    # %LOCALAPPDATA%\Packages\SocialPoint.DragonCityMobile_*
state = ClientState(packages_dir_path="C:/.../Packages", dragon_city_dir_name="SocialPoint.DragonCityMobile_abc")
```

| attribute | |
| --- | --- |
| `packages_dir_path`, `dragon_city_dir_name`, `dragon_city_dir_path` | where the package lives |
| `assets_dir_path` | `LocalCache/Local/Social Point/DragonCity` |
| `user_default_file_path` | `LocalCache/Local/DragonCity/UserDefault.xml` |
| `user_default` | `UserDefault` (raw entries) |
| `preferences` | `Preferences` (high level API) |
| `assets` | `Assets` |

`ClientState.find_dragon_city_dir_name(packages_dir_path=None)` locates the package folder. A missing
`LOCALAPPDATA`, packages folder or Dragon City package raises `ClientStateError`.

## `Preferences`

| method | |
| --- | --- |
| `set_farm_crop_range(plant_id, start, end)` | plant `plant_id` on crops `start` (inclusive) to `end` (exclusive) |
| `set_all_farm_crops(plant_id)`, `delete_all_farm_crops()`, `get_all_farm_crops()` | `retry_grow_type_food*` entries |
| `get_display_tutorials()`, `set_display_tutorials(shown)`, `delete_display_tutorials()` | entries containing `tutorial` |
| `disable_music()` / `enable_music()` | `options_music_disabled` |
| `disable_sound()` / `enable_sound()` | `options_sound_disabled` |
| `get_user_id()` | `int` or `None` |
| `get_last_execution()` | timezone-aware UTC `datetime` or `None` |
| `get_retry_breed_sanctuary_dragons()` | `RetrySanctuaryDragons(left_account_dragon_id, right_account_dragon_id)` or `None` |
| `set_retry_breed_sanctuary_dragons(left, right)` | |

## `UserDefault`

Low-level access to the `<entry key="...">value</entry>` list:

```python
user_default = UserDefault("UserDefault.xml")

user_default.get("user_origin_id")              # str or None
user_default.set("flag", True)                  # strings as is; anything else as JSON: "true", "12", '{"a":1}'
user_default.delete("flag")
user_default.list_by_prefix("retry_grow")       # [UserDefaultEntry(key, text)]
user_default.list_by_include("tutorial")
user_default.get_entries()

user_default.set_many([("a", 1), ("b", False)])   # one read + one write
user_default.delete_many(["a", "b"])
user_default.update_where(lambda key: "tutorial" in key, False)
```

The file is rewritten as UTF-8 with 4-space indentation, keeping its XML declaration.

## `Assets`

```python
from dc_client_state import AssetType

assets = state.assets
assets.list_assets()                                  # all files
assets.list_assets([AssetType.IMAGE, AssetType.AUDIO])
assets.set("ui_x.png", "my-replacement.png")          # overwrite a cached asset with another file
assets.delete("ui_x.png")
assets.get_file_path("ui_x.png")
assets.clear_assets()                                 # deletes every cached file
```

`AssetType` → extensions: `IMAGE` (`.png`, `.jpg`), `AUDIO` (`.mp3`, `.ogg`), `TEXTURE` (`.dds`), `MASK`
(`.mask`), `BINARY` (`.bin`).
