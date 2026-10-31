from enum import Enum


class AssetType(str, Enum):
    IMAGE = "image"
    AUDIO = "audio"
    TEXTURE = "texture"
    MASK = "mask"
    BINARY = "binary"

    def __str__(self) -> str:
        return str(self.value)
