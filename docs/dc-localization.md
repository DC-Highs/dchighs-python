# dc_localization

Download the translation files, look keys up, compare versions and translate configuration objects.
Port of `@dchighs/dc-localization`.

Extra: `localization` (`httpx`). Requires `dc_core`.

## Getting a `Localization`

```python
from dc_core import ConfigLanguage
from dc_localization import Localization

localization = await Localization.create(ConfigLanguage.ENGLISH)      # download + merge
raw = await Localization.fetch(ConfigLanguage.ENGLISH)                 # the raw array of {key: value}

localization = Localization(ConfigLanguage.ENGLISH, {"tid_a": "A"})    # from data you already have
```

`create`/`fetch` accept `client=` (an `httpx.AsyncClient`) and raise `LocalizationHttpError` on network or
HTTP-status failures. `Localization.build_url(language)` returns the file URL.

Attributes: `language`, `url`, `data` (`dict[str, str]`).

## Lookup

```python
localization.get_value_from_key("tid_unit_1000_name")
localization.get_key_from_value("Nature Dragon")      # first matching key
localization.get_dragon_name(1000)                    # tid_unit_<id>_name
localization.get_dragon_description(1000)             # tid_unit_<id>_description
localization.get_attack_name(1)                       # tid_attack_name_<id>
localization.get_skill_name(1)                        # tid_skill_name_<id>
localization.get_skill_description(1)                 # tid_skill_description_<id>
```

All return `None` when the key does not exist.

## Searching

```python
localization.search_values("epico")        # matches "Épico": case and accent insensitive
localization.search_keys("chest")
localization.search_values("Épico", NormalizeOptions(normalize_letters=False))
```

`NormalizeOptions(lower_case=True, normalize_letters=True, trim_spaces=True)`.

## Comparing versions

```python
diff = old.compare(new)                     # or Localization.compare_between(old, new)
diff.new_fields       # [ComparisonResultNewField(key, value)]
diff.edited_fields    # [ComparisonResultEditedField(key, values=ComparisonResultEditedFieldValues(old, new))]
diff.deleted_fields   # [ComparisonResultDeletedField(key, value)]
```

Comparing localizations of different languages raises `LanguageMismatchError`.

## Translating objects

`translate(obj)` returns a copy of a dict where translation keys are replaced by their text:

| key(s) | becomes |
| --- | --- |
| `tid_name`, `chest_name_key`, `name_key`, `island_title_tid` (and camelCase forms) | `name` |
| `type_name_key`, `typeNameKey` | `type_name` |
| `description_key`, `tid_description` (and camelCase forms) | `description` |

Keys with no (or an empty) translation are left untouched. Only the top level is translated; non-dicts are
returned as is. `translate_object(obj)` does the same in place. The key lists are exported as
`NAME_KEYS_TO_TRANSLATE`, `TYPE_NAME_KEYS_TO_TRANSLATE` and `DESCRIPTION_KEYS_TO_TRANSLATE`.

```python
localization.translate({"id": 1, "chest_name_key": "tid_chest"})   # {"id": 1, "name": "Chest"}
```

`to_array()` converts back to the original array-of-single-pairs format.
