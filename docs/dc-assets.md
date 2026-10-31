# dc_assets

Download static assets (sprites, thumbnails, animations, island packages, music) from the Dragon City servers.
Port of `@dchighs/dc-assets`.

Extra: `assets` (`httpx`). Requires `dc_core`.

## Downloaders

Each downloader is a small object that knows its URL:

```python
from dc_assets import DragonSpriteDownloader
from dc_core import DragonPhase, SpriteQuality

sprite = DragonSpriteDownloader("1000_dragon_nature", DragonPhase.ADULT, skin="_1", image_quality=SpriteQuality.LARGE)

sprite.url                          # .../mobile/ui/dragons/ui_1000_dragon_nature_1_3@2x.png
data: bytes = await sprite.fetch()  # in memory
path = await sprite.download("dragon.png")   # to disk, returns a pathlib.Path
```

- `fetch(client=None)` / `download(path, client=None)` accept an `httpx.AsyncClient`.
- `urls` lists the candidates; the first one answering with a successful status wins.
- Failures raise `AssetsHttpError`; disk errors raise `AssetsError` (the base class).

`platform_prefix` (default `StaticFileUrlPlatformPrefix.IOS` → `dci`) accepts the enum or a string.

| class | arguments (besides `platform_prefix`) | file |
| --- | --- | --- |
| `DragonSpriteDownloader` | `image_name`, `phase`, `skin=None`, `image_quality` | `ui_<image><skin>_<phase><quality>.png` |
| `DragonThumbnailDownloader` | `image_name`, `phase`, `skin=None` | `thumb_<image><skin>_<phase>.png` |
| `DragonFlashAnimationDownloader` | `image_name`, `phase`, `skin=None` | `.swf` |
| `DragonSpineAnimationDownloader` | `image_name`, `phase`, `skin=None`, `texture_compression_format`, `use_new_url_format=True` | `.zip` (`_HD_tweened_` or legacy `basic_..._spine-3-8-59`) |
| `BuildingSpriteDownloader`, `DecorationSpriteDownloader`, `HabitatSpriteDownloader` | `image_name`, `image_quality` | `ui_<image><quality>.png` |
| `BuildingThumbnailDownloader`, `DecorationThumbnailDownloader`, `HabitatThumbnailDownloader` | `image_name` | `<image>.jpg` |
| `ChestSpriteDownloader` | `image_name`, `image_quality` | tries `ui_<image>…`, then falls back to `ui_basic_<image>…` (`basic_url`) |
| `IslandPackageDownloader` | `island_type`, `file_name` | island `.zip` |
| `MusicDownloader` | `key_name` | `.mp3` (plain HTTP, as served by the game) |
| `FlashClientDownloader` | `version` | `flash/Base_sec_<version>.swf`: the Flash client itself |

`phase` accepts a `DragonPhase` or an `int`.

### Island packages

```python
IslandPackageDownloader(IslandType.HEROIC_RACES, "a.zip")          # heroicraces_islands/HD/dxt5/a.zip
IslandPackageDownloader("grid_islands", "a.zip")                    # file becomes a_optim.zip
IslandPackageDownloader.from_path("/static/dragoncity/maze_islands/file.zip")   # from a config `zip_file`
```

`from_path` takes the island type from the 4th and the file name from the 5th `/`-separated segment and raises
`InvalidArgumentsError` (a `ValueError`) when they are missing.

### Music

`dc_core.get_music_name_from_tag(sound_tag)` resolves the key name from an island's `sound_tag`:

```python
name = get_music_name_from_tag("FANTASY")
await MusicDownloader(name).download(f"{name}.mp3")
```

Reusing one client for many downloads:

```python
async with httpx.AsyncClient() as client:
    for downloader in downloaders:
        await downloader.download(f"out/{downloader.url.rsplit('/', 1)[-1]}", client)
```

### Flash client versions

Old versions of the Flash client are still served by the static servers:

```python
client = FlashClientDownloader("2.2.5")
client.url    # https://dci-static-s1.socialpointgames.com/static/dragoncity/flash/Base_sec_2.2.5.swf
await client.download("Base_sec_2.2.5.swf")
```

A version that does not exist answers with an HTTP error, raised as `AssetsHttpError`.
