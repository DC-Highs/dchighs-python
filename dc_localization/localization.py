import unicodedata
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import httpx

from dc_core import ConfigLanguage
from dc_localization.keys import (
    DESCRIPTION_KEYS_TO_TRANSLATE,
    NAME_KEYS_TO_TRANSLATE,
    TYPE_NAME_KEYS_TO_TRANSLATE,
)

LocalizationData = Dict[str, str]


class LocalizationError(Exception):
    """Base class of the errors of this package."""


class LocalizationHttpError(LocalizationError):
    """The request failed or the server answered with a non-2xx status."""


class LanguageMismatchError(LocalizationError, ValueError):
    """Two localizations of different languages were compared."""

    def __init__(self, left: ConfigLanguage, right: ConfigLanguage) -> None:
        self.left = left
        self.right = right
        super().__init__(f"languages do not match: {left} != {right}")


@dataclass(frozen=True)
class ComparisonResultNewField:
    key: str
    value: str


@dataclass(frozen=True)
class ComparisonResultEditedFieldValues:
    old: str
    new: str


@dataclass(frozen=True)
class ComparisonResultEditedField:
    key: str
    values: ComparisonResultEditedFieldValues


@dataclass(frozen=True)
class ComparisonResultDeletedField:
    key: str
    value: str


@dataclass
class ComparisonResult:
    new_fields: List[ComparisonResultNewField] = field(default_factory=list)
    edited_fields: List[ComparisonResultEditedField] = field(default_factory=list)
    deleted_fields: List[ComparisonResultDeletedField] = field(default_factory=list)


@dataclass(frozen=True)
class NormalizeOptions:
    """Text normalization used by :meth:`Localization.search_keys` and
    :meth:`Localization.search_values`. Everything is enabled by default."""

    lower_case: bool = True
    normalize_letters: bool = True
    trim_spaces: bool = True

    def apply(self, text: str) -> str:
        result = text

        if self.lower_case:
            result = result.lower()

        if self.normalize_letters:
            result = "".join(
                char
                for char in unicodedata.normalize("NFD", result)
                if not ("̀" <= char <= "ͯ")
            )

        if self.trim_spaces:
            result = result.strip()

        return result


class Localization:
    """Translations of the game for one language."""

    def __init__(self, language: ConfigLanguage, data: LocalizationData) -> None:
        self.language = ConfigLanguage(language)
        self.url = self.build_url(self.language)
        self.data = data

    def __repr__(self) -> str:
        return f"Localization(language={self.language.value!r}, entries={len(self.data)})"

    @staticmethod
    def build_url(language: ConfigLanguage) -> str:
        return (
            "https://sp-translations.socialpointgames.com/deploy/dc/android/prod/"
            f"dc_android_{ConfigLanguage(language)}_prod_wetd46pWuR8J5CmS.json"
        )

    @classmethod
    async def fetch(
        cls,
        language: ConfigLanguage = ConfigLanguage.ENGLISH,
        client: Optional[httpx.AsyncClient] = None,
    ) -> List[LocalizationData]:
        """Downloads the raw translation file (an array of small key/value objects)."""
        url = cls.build_url(language)

        try:
            if client is not None:
                response = await client.get(url)
            else:
                async with httpx.AsyncClient() as own_client:
                    response = await own_client.get(url)

            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as error:
            raise LocalizationHttpError(f"http error: {error}") from error

    @classmethod
    async def create(
        cls,
        language: ConfigLanguage = ConfigLanguage.ENGLISH,
        client: Optional[httpx.AsyncClient] = None,
    ) -> "Localization":
        """Downloads and merges the translation file for ``language``."""
        array_data = await cls.fetch(language, client)
        data: LocalizationData = {}

        for entry in array_data:
            data.update(entry)

        return cls(language, data)

    def get_value_from_key(self, key: str) -> Optional[str]:
        return self.data.get(key)

    def get_key_from_value(self, value: str) -> Optional[str]:
        for key, candidate in self.data.items():
            if candidate == value:
                return key

        return None

    def get_dragon_name(self, id: int) -> Optional[str]:
        return self.get_value_from_key(f"tid_unit_{id}_name")

    def get_dragon_description(self, id: int) -> Optional[str]:
        return self.get_value_from_key(f"tid_unit_{id}_description")

    def get_attack_name(self, id: int) -> Optional[str]:
        return self.get_value_from_key(f"tid_attack_name_{id}")

    def get_skill_name(self, id: int) -> Optional[str]:
        return self.get_value_from_key(f"tid_skill_name_{id}")

    def get_skill_description(self, id: int) -> Optional[str]:
        return self.get_value_from_key(f"tid_skill_description_{id}")

    def search_keys(self, query: str, options: Optional[NormalizeOptions] = None) -> List[str]:
        """Keys that contain ``query`` (accent/case-insensitive by default)."""
        options = options or NormalizeOptions()
        normalized = options.apply(query)
        return [key for key in self.data if normalized in options.apply(key)]

    def search_values(self, query: str, options: Optional[NormalizeOptions] = None) -> List[str]:
        """Values that contain ``query`` (accent/case-insensitive by default)."""
        options = options or NormalizeOptions()
        normalized = options.apply(query)
        return [value for value in self.data.values() if normalized in options.apply(value)]

    def to_array(self) -> List[LocalizationData]:
        return [{key: value} for key, value in self.data.items()]

    def compare(self, other: "Localization") -> ComparisonResult:
        """Differences between ``self`` (old) and ``other`` (new)."""
        return Localization.compare_between(self, other)

    @staticmethod
    def compare_between(old: "Localization", new: "Localization") -> ComparisonResult:
        """Differences between ``old`` and ``new``."""
        if old.language != new.language:
            raise LanguageMismatchError(old.language, new.language)

        result = ComparisonResult()

        for key, new_value in new.data.items():
            if key not in old.data:
                result.new_fields.append(ComparisonResultNewField(key, new_value))
            elif old.data[key] != new_value:
                result.edited_fields.append(
                    ComparisonResultEditedField(
                        key, ComparisonResultEditedFieldValues(old=old.data[key], new=new_value)
                    )
                )

        for key, old_value in old.data.items():
            if key not in new.data:
                result.deleted_fields.append(ComparisonResultDeletedField(key, old_value))

        return result

    def translate(self, value: Any) -> Any:
        """Replaces the translation keys of a dict (``name_key``, ``tid_name``, ``type_name_key``,
        ``description_key``, ...) by the translated ``name``, ``type_name`` and ``description``.

        Keys without a translation are kept as is. Only the top level is translated and the
        input is not modified; anything that is not a dict is returned unchanged.
        """
        if not isinstance(value, dict):
            return value

        translated = dict(value)
        self.translate_object(translated)
        return translated

    def translate_object(self, obj: Dict[str, Any]) -> None:
        """Same as :meth:`translate`, modifying ``obj`` in place."""
        for key in list(obj.keys()):

            def translation_of() -> Optional[str]:
                translation_key = obj.get(key)

                if not isinstance(translation_key, str):
                    return None

                translated = self.get_value_from_key(translation_key)
                return translated if translated else None

            if key in NAME_KEYS_TO_TRANSLATE:
                name = translation_of()

                if name is not None:
                    obj["name"] = name
                    obj.pop(key, None)
            elif key in TYPE_NAME_KEYS_TO_TRANSLATE:
                type_name = translation_of()

                if type_name is not None:
                    obj["type_name"] = type_name
                    obj.pop(key, None)

            if key in DESCRIPTION_KEYS_TO_TRANSLATE:
                description = translation_of()

                if description is not None:
                    obj["description"] = description
                    obj.pop(key, None)
