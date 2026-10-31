"""Dragon City localization: download the translation files, look keys up and translate
configuration objects.

Fan-made library, not affiliated with SocialPoint.
"""

from dc_localization.keys import (
    DESCRIPTION_KEYS_TO_TRANSLATE,
    NAME_KEYS_TO_TRANSLATE,
    TYPE_NAME_KEYS_TO_TRANSLATE,
)
from dc_localization.localization import (
    ComparisonResult,
    ComparisonResultDeletedField,
    ComparisonResultEditedField,
    ComparisonResultEditedFieldValues,
    ComparisonResultNewField,
    LanguageMismatchError,
    Localization,
    LocalizationData,
    LocalizationError,
    LocalizationHttpError,
    NormalizeOptions,
)

__all__ = [
    "ComparisonResult",
    "ComparisonResultDeletedField",
    "ComparisonResultEditedField",
    "ComparisonResultEditedFieldValues",
    "ComparisonResultNewField",
    "DESCRIPTION_KEYS_TO_TRANSLATE",
    "LanguageMismatchError",
    "Localization",
    "LocalizationData",
    "LocalizationError",
    "LocalizationHttpError",
    "NAME_KEYS_TO_TRANSLATE",
    "NormalizeOptions",
    "TYPE_NAME_KEYS_TO_TRANSLATE",
]
