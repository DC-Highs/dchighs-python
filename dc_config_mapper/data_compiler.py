from typing import Any, Dict, Iterable, List, Mapping, Optional

from pluralizer import Pluralizer

from dc_config_mapper.errors import InvalidContextError, MaxDepthExceededError
from dc_config_mapper.utils import is_number, truthy

MAX_DEPTH = 128

_pluralizer = Pluralizer()


def _pluralize(word: str) -> str:
    return _pluralizer.pluralize(word, 2, False)


class CompileContext:
    """Named collections (``"dragons"``, ``"attacks"``, ``"rewards"``, ...) used to resolve ids.

    Each element of a collection needs an ``id``.
    """

    def __init__(self, collections: Optional[Mapping[str, Any]] = None) -> None:
        self.collections: Dict[str, Any] = dict(collections or {})

    def with_collection(self, key: str, collection: Iterable[Any]) -> "CompileContext":
        """Adds a collection and returns ``self``, e.g. ``.with_collection("dragons", items.dragons)``."""
        self.collections[key] = list(collection)
        return self

    def insert(self, key: str, collection: Any) -> None:
        self.collections[key] = collection


def _same_id(item_id: Any, wanted: Any) -> bool:
    """``item.id === id`` (``1`` and ``1.0`` are the same number in JavaScript)."""
    if is_number(item_id) and is_number(wanted):
        return float(item_id) == float(wanted)

    if isinstance(item_id, bool) or isinstance(wanted, bool):
        return isinstance(item_id, bool) and isinstance(wanted, bool) and item_id == wanted

    return item_id is not None and item_id == wanted


class DataCompiler:
    """Resolves id references in mapped data using a :class:`CompileContext`:

    * ``"dragon_id": 5`` becomes ``"dragon": { ...dragon 5... }``
    * ``"reward_ids": [1, 2]`` becomes ``"rewards": [ {...}, {...} ]``

    Resolved items are compiled recursively. Keys may carry one of the ``accepted_prefixes``
    (``"basic_attack_ids"`` with prefix ``"basic_"`` becomes ``"basic_attacks"``).
    """

    def __init__(
        self,
        accepted_prefixes: Optional[Iterable[str]] = None,
        ids_suffix: str = "_ids",
        id_suffix: str = "_id",
    ) -> None:
        self.accepted_prefixes: List[str] = list(accepted_prefixes or [])
        self.ids_suffix = ids_suffix
        self.id_suffix = id_suffix

    def compile(self, data: Any, context: CompileContext) -> Any:
        """Returns a compiled copy of ``data``."""
        return self._compile_value(data, context.collections, 0)

    def compile_many(self, data: Iterable[Any], context: CompileContext) -> List[Any]:
        return [self.compile(item, context) for item in data]

    def _compile_value(self, value: Any, context: Mapping[str, Any], depth: int) -> Any:
        if depth > MAX_DEPTH:
            raise MaxDepthExceededError(MAX_DEPTH)

        if isinstance(value, dict):
            return self._compile_object(value, context, depth)

        if isinstance(value, list):
            return [self._compile_value(item, context, depth + 1) for item in value]

        return value

    def _matching_prefix(self, key: str) -> str:
        for prefix in self.accepted_prefixes:
            if key.startswith(prefix):
                return prefix

        return ""

    @staticmethod
    def _base_key(key: str, prefix: str, suffix: str) -> str:
        rest = key[len(prefix):]
        return rest[: max(len(rest) - len(suffix), 0)]

    @staticmethod
    def _collection(context: Mapping[str, Any], name: str) -> Optional[List[Any]]:
        collection = context.get(name)

        if not truthy(collection):
            return None

        if not isinstance(collection, list):
            raise InvalidContextError(name)

        return collection

    def _compile_object(self, original: Dict[str, Any], context: Mapping[str, Any], depth: int) -> Dict[str, Any]:
        data = dict(original)

        for key, value in original.items():
            if isinstance(value, (list, dict)):
                data[key] = self._compile_value(value, context, depth + 1)

            prefix = self._matching_prefix(key)

            if key.endswith(self.ids_suffix) and isinstance(value, list):
                base = self._base_key(key, prefix, self.ids_suffix)
                plural = _pluralize(base)
                items = self._collection(context, plural)

                if items is not None:
                    related = []

                    for wanted in value:
                        found = next(
                            (item for item in items if _same_id(item.get("id") if isinstance(item, dict) else None, wanted)),
                            None,
                        )

                        if found is not None:
                            related.append(self._compile_value(found, context, depth + 1))

                    data[f"{prefix}{plural}"] = related
                    data.pop(key, None)
            elif key.endswith(self.id_suffix) and truthy(value):
                base = self._base_key(key, prefix, self.id_suffix)
                plural = _pluralize(base)
                items = self._collection(context, plural)

                if items is not None:
                    found = next(
                        (item for item in items if _same_id(item.get("id") if isinstance(item, dict) else None, value)),
                        None,
                    )
                    compiled = self._compile_value(found, context, depth + 1) if found is not None else None

                    data[f"{prefix}{base}"] = compiled
                    data.pop(key, None)

        return data
