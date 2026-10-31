"""Helpers shared by the schemas and mappers (ports of the ``utils`` of the TypeScript package)."""

import math
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Union

from pydantic import StrictFloat, StrictInt
from pydantic import ValidationError as PydanticValidationError

from dc_config_mapper.errors import (
    DecorationPositionMismatchError,
    InvalidBooleanError,
    InvalidNumberError,
    InvalidTimestampError,
    MissingFieldError,
    SchemaError,
    UnexpectedPriceError,
    UnprocessedRewardsError,
)
from dc_core import DragonElement

Num = Union[StrictInt, StrictFloat]

JsonDict = Dict[str, Any]

_EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def number_to_boolean(n: Any) -> bool:
    """``numberToBoolean``: only ``0`` and ``1`` are accepted."""
    if is_number(n):
        if n == 1:
            return True

        if n == 0:
            return False

    raise InvalidBooleanError(n)


def iso_from_ts(ts: Any) -> str:
    """``new Date(ts * 1000).toISOString()``."""
    try:
        millis = int(ts * 1000)
        moment = _EPOCH + timedelta(milliseconds=millis)
    except (OverflowError, ValueError, TypeError) as error:
        raise InvalidTimestampError(ts) from error

    return f"{moment.strftime('%Y-%m-%dT%H:%M:%S')}.{moment.microsecond // 1000:03d}Z"


def basename(path: str) -> str:
    """``path.basename``."""
    return path.rstrip("/\\").replace("\\", "/").rsplit("/", 1)[-1]


def _from_float(value: float, what: str) -> Num:
    if not math.isfinite(value):
        raise InvalidNumberError(what)

    if value == int(value) and abs(value) < 9.0e15:
        return int(value)

    return value


def num_sub(a: Num, b: Num) -> Num:
    """``a - b`` keeping integers as integers."""
    if isinstance(a, int) and isinstance(b, int):
        return a - b

    return _from_float(float(a) - float(b), f"{a} - {b}")


def num_mul(a: Num, b: Num) -> Num:
    """``a * b`` keeping integers as integers."""
    if isinstance(a, int) and isinstance(b, int):
        return a * b

    return _from_float(float(a) * float(b), f"{a} * {b}")


def truthy(value: Any) -> bool:
    """JavaScript truthiness of a JSON value."""
    if value is None:
        return False

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        return value != 0 and not (isinstance(value, float) and math.isnan(value))

    if isinstance(value, str):
        return value != ""

    return True


def process_price(gem: Optional[Num] = None, gold: Optional[Num] = None) -> Optional[JsonDict]:
    """``processPrice``: ``{ g: 10 }`` -> ``{ type: gold, amount: 10 }``, ``{}`` -> ``None``."""
    if gold is None and gem is None:
        return None

    if gold is not None and gem is None:
        return {"type": "gold", "amount": gold}

    if gold is None and gem is not None:
        return {"type": "gem", "amount": gem}

    raise UnexpectedPriceError(f'multiple price keys: {{"g":{gold},"c":{gem}}}')


_PET_FOOD_PACK_SIZES = ("s", "m", "l", "xl")


def _truthy_entry(reward: Mapping[str, Any], key: str) -> Any:
    value = reward.get(key)
    return value if truthy(value) else None


def _number_of(value: Any, what: str) -> Num:
    if not is_number(value):
        raise UnprocessedRewardsError(f"{what} is not a number: {value!r}")

    return value


def _reward(kind: str, **fields: Any) -> JsonDict:
    """A normalized reward; fields that are ``None`` are left out."""
    order = (
        "element",
        "amount",
        "chest_id",
        "dragon_id",
        "dragon_ids",
        "building_id",
        "orb_dragon_id",
        "size",
    )
    reward: JsonDict = {"type": kind}

    for key in order:
        value = fields.get(key)

        if value is not None:
            reward[key] = value

    return reward


def process_rewards(rewards: Iterable[Mapping[str, Any]]) -> List[JsonDict]:
    """``processRewards``: turns the compact reward objects of the game
    (``{"g": 10}``, ``{"egg": 1042}``, ``{"el_token": 3}``, ...) into normalized rewards
    (``{"type": "gold", "amount": 10}``, ...)."""
    rewards = list(rewards)
    filtered = [reward for reward in rewards if reward]
    processed: List[JsonDict] = []

    for reward in filtered:
        chest = _truthy_entry(reward, "chest")

        if chest is not None:
            processed.append(_reward("chest", chest_id=_number_of(chest, "chest")))

        egg = _truthy_entry(reward, "egg")

        if egg is not None:
            if isinstance(egg, list):
                processed.append(_reward("dragon", dragon_ids=[_number_of(item, "egg") for item in egg]))
            else:
                processed.append(_reward("dragon", dragon_id=_number_of(egg, "egg")))

        for key, kind in (("g", "gold"), ("c", "gem"), ("f", "food")):
            amount = _truthy_entry(reward, key)

            if amount is not None:
                processed.append(_reward(kind, amount=_number_of(amount, key)))

        building = _truthy_entry(reward, "b")

        if building is not None:
            if isinstance(building, list):
                building_id = _number_of(building[0], "b") if building else None
            else:
                building_id = _number_of(building, "b")

            processed.append(_reward("building", building_id=building_id))

        event_points = _truthy_entry(reward, "ep")

        if event_points is not None:
            processed.append(_reward("event_points", amount=_number_of(event_points, "ep")))

        seeds = _truthy_entry(reward, "seeds")

        if seeds is not None:
            for seed in seeds if isinstance(seeds, list) else []:
                seed = seed if isinstance(seed, dict) else {}
                processed.append(
                    _reward(
                        "dragon_orbs",
                        orb_dragon_id=_number_of(seed.get("id"), "seeds.id"),
                        amount=_number_of(seed.get("amount"), "seeds.amount"),
                    )
                )

        energy = _truthy_entry(reward, "en_runner")

        if energy is not None:
            processed.append(_reward("runner_island_energy", amount=_number_of(energy, "en_runner")))

        token_key = next((key for key in reward if key.endswith("_token")), None)

        if token_key is not None:
            acronym = token_key.split("_")[0]

            if not acronym:
                raise UnprocessedRewardsError("invalid reward")

            element = DragonElement.from_acronym(acronym)
            processed.append(
                _reward(
                    "habitat_token",
                    element=element.value if element is not None else None,
                    amount=_number_of(reward[token_key], token_key),
                )
            )

        for size in _PET_FOOD_PACK_SIZES:
            key = f"pet_food_pack.{size}"

            if key in reward:
                processed.append(_reward("pet_food_pack", size=size, amount=_number_of(reward[key], key)))

        pack_key = next((key for key in reward if key.startswith("album_pack_aces.")), None)

        if pack_key is not None:
            size = pack_key.rsplit(".", 1)[-1]

            if not size:
                raise UnprocessedRewardsError("invalid reward")

            processed.append(
                _reward("album_pack_aces", size=size, amount=_number_of(reward[pack_key], pack_key))
            )

    if len(processed) < len(filtered):
        import json

        raise UnprocessedRewardsError(
            f"{json.dumps(rewards, default=str)} -> {json.dumps(processed, default=str)}"
        )

    return processed


def _coordinate(value: Any, key: str) -> int:
    found = value.get(key) if isinstance(value, dict) else None

    if not is_number(found):
        raise MissingFieldError(key)

    return int(found)


def resolve_grid_decoration_positions(
    squares: Sequence[JsonDict],
    decorations: Sequence[JsonDict],
    board_width: int,
    board_height: int,
) -> List[JsonDict]:
    """``resolveGridDecorationPositions``: grid decorations come without coordinates; they occupy,
    in order, the board cells that are not squares.

    ``squares`` and ``decorations`` are the raw ``grid_island.squares``/``grid_island.decorations``
    objects; the returned decorations get their ``x``/``y`` filled in.
    """
    taken = {(_coordinate(square, "x"), _coordinate(square, "y")) for square in squares}

    positions = [
        (x, y)
        for x in range(1, board_width + 1)
        for y in range(1, board_height + 1)
        if (x, y) not in taken
    ]

    if len(positions) != len(decorations):
        raise DecorationPositionMismatchError()

    resolved: List[JsonDict] = []

    for decoration, (x, y) in zip(decorations, positions):
        item = dict(decoration)
        item["x"] = x
        item["y"] = y
        resolved.append(item)

    return resolved


def parse(schema: str, model: Any, value: Any) -> Any:
    """Validates ``value`` against a strict schema, tagging the error with the schema name."""
    try:
        return model.model_validate(value)
    except PydanticValidationError as error:
        raise SchemaError(schema, error) from error


def with_fields(value: Mapping[str, Any], **fields: Any) -> JsonDict:
    """Copy of an object with extra fields injected (what the TS mappers do with ``{ ...item, extra }``)."""
    copy = dict(value)
    copy.update(fields)
    return copy


def array(section: Any, key: str) -> List[Any]:
    """Required array of a section."""
    value = section.get(key) if isinstance(section, dict) else None

    if not isinstance(value, list):
        raise MissingFieldError(key)

    return value


def ids_where(items: Sequence[Any], field: str, owner: Mapping[str, Any]) -> List[Any]:
    """Ids (``id`` field) of the elements of ``items`` whose ``field`` equals the ``id`` of ``owner``."""
    if "id" not in owner:
        return []

    owner_id = owner["id"]

    return [
        item["id"]
        for item in items
        if isinstance(item, dict) and field in item and item[field] == owner_id and "id" in item
    ]


def passthrough(section: Any, key: str) -> Any:
    """Section value to copy as-is (``None`` when absent, so it is left out of the result)."""
    return section.get(key) if isinstance(section, dict) else None


def size_from_pair(values: Sequence[Num]) -> JsonDict:
    """``[width, height]`` -> ``{"width": ..., "height": ...}`` (missing values are left out)."""
    size: JsonDict = {}

    if len(values) > 0:
        size["width"] = values[0]

    if len(values) > 1:
        size["height"] = values[1]

    return size


def availability_from_ts(start: Num, end: Num) -> JsonDict:
    return {"from": iso_from_ts(start), "to": iso_from_ts(end)}


def put(target: JsonDict, **fields: Any) -> JsonDict:
    """Adds the fields that are not ``None`` (serde's ``skip_serializing_if = "Option::is_none"``)."""
    for key, value in fields.items():
        if value is not None:
            target[key] = value

    return target
