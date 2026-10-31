import shutil
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Union

from dc_client_state.enums import AssetType

EXTENSION_MAP: Dict[AssetType, Tuple[str, ...]] = {
    AssetType.IMAGE: (".png", ".jpg"),
    AssetType.AUDIO: (".mp3", ".ogg"),
    AssetType.TEXTURE: (".dds",),
    AssetType.MASK: (".mask",),
    AssetType.BINARY: (".bin",),
}


class Assets:
    """The assets cached by the game client (replace or remove them to customize the game)."""

    def __init__(self, assets_dir_path: Union[str, Path]) -> None:
        self.assets_dir_path = Path(assets_dir_path)

    def set(self, current_asset_file_name: str, substitute_asset_file_path: Union[str, Path]) -> None:
        """Replaces the cached asset ``current_asset_file_name`` with the content of another file."""
        shutil.copyfile(substitute_asset_file_path, self.get_file_path(current_asset_file_name))

    def delete(self, asset_file_name: str) -> None:
        self.get_file_path(asset_file_name).unlink()

    def get_file_path(self, asset_file_name: str) -> Path:
        return self.assets_dir_path / asset_file_name

    def list_assets(self, asset_types: Optional[Iterable[AssetType]] = None) -> List[Path]:
        """Paths of the cached files, optionally only those of the given asset types."""
        file_paths = sorted(self.assets_dir_path.iterdir())

        if asset_types is None:
            return file_paths

        extensions = tuple(
            extension
            for asset_type in asset_types
            for extension in EXTENSION_MAP.get(AssetType(asset_type), ())
        )

        return [path for path in file_paths if str(path).endswith(extensions)]

    def clear_assets(self) -> None:
        """Deletes every cached file."""
        for path in self.assets_dir_path.iterdir():
            if path.is_file() or path.is_symlink():
                path.unlink()
