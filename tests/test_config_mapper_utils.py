import pytest

from dc_config_mapper import (
    CompileContext,
    DataCompiler,
    InvalidBooleanError,
    InvalidContextError,
    InvalidNumberError,
    InvalidTimestampError,
    MissingFieldError,
    UnprocessedRewardsError,
    iso_from_ts,
    number_to_boolean,
    process_rewards,
    resolve_grid_decoration_positions,
)
from dc_config_mapper.errors import (
    DecorationPositionMismatchError,
    MapperError,
    MaxDepthExceededError,
    RewardNotFoundError,
    SchemaError,
    UnexpectedPriceError,
    UnprocessedRewardsError as UnprocessedRewards,
)
from dc_config_mapper.schemas.base import coerce_number, coerce_number_list
from dc_config_mapper.utils import (
    array,
    basename,
    ids_where,
    is_number,
    num_mul,
    num_sub,
    parse,
    passthrough,
    size_from_pair,
    truthy,
    with_fields,
)
from dc_config_mapper.schemas.fog import FogRewardIn


def test_number_helpers():
    assert is_number(1) and is_number(1.5) and not is_number(True) and not is_number("1")
    assert number_to_boolean(1.0) is True

    for invalid in ("1", True, None, 2):
        with pytest.raises(InvalidBooleanError):
            number_to_boolean(invalid)

    assert num_sub(5, 2) == 3 and num_sub(5.5, 0.5) == 5 and isinstance(num_sub(5.5, 0.5), int)
    assert num_sub(5.5, 1) == 4.5
    assert num_mul(2, 3) == 6 and num_mul(1.5, 3) == 4.5 and num_mul(2.5, 2) == 5

    with pytest.raises(InvalidNumberError):
        num_mul(float("inf"), 2.5)


def test_truthiness_follows_javascript():
    assert [truthy(v) for v in (None, False, True, 0, 0.0, 1, float("nan"), "", "a", [], {}, [0])] == [
        False, False, True, False, False, True, False, False, True, True, True, True,
    ]


def test_timestamps_and_paths():
    with pytest.raises(InvalidTimestampError):
        iso_from_ts(1e20)

    with pytest.raises(InvalidTimestampError):
        iso_from_ts("1")

    assert iso_from_ts(-1) == "1969-12-31T23:59:59.000Z"
    assert basename("a\\b\\c.zip") == "c.zip" and basename("dir/") == "dir" and basename("") == ""


def test_json_helpers():
    assert array({"a": [1]}, "a") == [1]

    for section in ({"a": 1}, {}, None, [1]):
        with pytest.raises(MissingFieldError):
            array(section, "a")

    assert passthrough({"a": 1}, "a") == 1 and passthrough({}, "a") is None and passthrough(None, "a") is None
    assert with_fields({"a": 1}, b=2) == {"a": 1, "b": 2}
    assert size_from_pair([]) == {} and size_from_pair([1]) == {"width": 1} and size_from_pair([1, 2, 3]) == {
        "width": 1, "height": 2,
    }

    items = [{"id": 1, "o": 5}, {"id": 2, "o": 6}, {"o": 5}, {"id": 4}, "x"]
    assert ids_where(items, "o", {"id": 5}) == [1]
    assert ids_where(items, "o", {}) == []


def test_parse_wraps_pydantic_errors():
    with pytest.raises(SchemaError) as error:
        parse("fog reward", FogRewardIn, {"id": 1})

    assert error.value.schema == "fog reward"
    assert isinstance(error.value, MapperError)
    assert str(error.value).startswith("invalid fog reward: ")


def test_coerce_numbers():
    assert coerce_number(True) == 1 and coerce_number(None) == 0 and coerce_number(" ") == 0
    assert coerce_number(" 12 ") == 12 and coerce_number("1.5") == 1.5 and coerce_number(3) == 3

    for invalid in ("abc", "nan", "1_0", {"a": 1}, [1]):
        with pytest.raises(ValueError):
            coerce_number(invalid)

    assert coerce_number_list(None) is None and coerce_number_list(["1"]) == [1]

    with pytest.raises(ValueError):
        coerce_number_list("1")


def test_reward_edge_cases():
    assert process_rewards([{"b": []}]) == [{"type": "building"}]
    assert process_rewards([{"seeds": "nope", "g": 1}]) == [{"type": "gold", "amount": 1}]
    assert process_rewards([{"zz_token": 4}]) == [{"type": "habitat_token", "amount": 4}]

    for invalid in (
        [{"g": "10"}],
        [{"egg": "x"}],
        [{"egg": ["x"]}],
        [{"b": "x"}],
        [{"b": ["x"]}],
        [{"seeds": [{"id": 1}]}],
        [{"seeds": [3]}],
        [{"_token": 1}],
        [{"el_token": "x"}],
        [{"pet_food_pack.s": "x"}],
        [{"album_pack_aces.": 1}],
        [{"album_pack_aces.big": "x"}],
        [{"unknown": 1}],
        [{"g": 0}],
    ):
        with pytest.raises(UnprocessedRewards):
            process_rewards(invalid)

    assert issubclass(UnprocessedRewards, MapperError) and UnprocessedRewardsError is UnprocessedRewards


def test_grid_decoration_positions_validate_squares():
    with pytest.raises(MissingFieldError):
        resolve_grid_decoration_positions([{"x": 1}], [], 1, 1)

    with pytest.raises(MissingFieldError):
        resolve_grid_decoration_positions(["x"], [], 1, 1)

    with pytest.raises(DecorationPositionMismatchError):
        resolve_grid_decoration_positions([], [], 1, 1)

    assert resolve_grid_decoration_positions([{"x": 1, "y": 1}], [], 1, 1) == []


def test_error_messages():
    assert "reward 3 not found" in str(RewardNotFoundError(3))
    assert "unexpected price" in str(UnexpectedPriceError("x"))
    assert "depth of 128" in str(MaxDepthExceededError(128))
    assert "`ctx`" in str(InvalidContextError("ctx"))


def context():
    return CompileContext({"dragons": [{"id": 1, "name": "A"}, {"id": 2.0, "name": "B"}, {"name": "no id"}, 7]})


def test_compile_context_and_ids():
    ctx = CompileContext()
    ctx.insert("attacks", [{"id": 1}])
    ctx.with_collection("rewards", iter([{"id": 2}]))
    compiler = DataCompiler()

    assert compiler.compile({"attack_id": 1, "reward_ids": [2]}, ctx) == {"attack": {"id": 1}, "rewards": [{"id": 2}]}
    assert compiler.compile({"dragon_id": 2}, context()) == {"dragon": {"id": 2.0, "name": "B"}}
    assert compiler.compile({"dragon_id": "x"}, context()) == {"dragon": None}
    assert compiler.compile({"dragon_ids": [True, "x", 1.0]}, context()) == {"dragons": [{"id": 1, "name": "A"}]}
    assert compiler.compile({"dragon_ids": 5, "dragon_id": 0}, context()) == {"dragon_ids": 5, "dragon_id": 0}
    assert compiler.compile_many([{"dragon_id": 1}, 5], context()) == [{"dragon": {"id": 1, "name": "A"}}, 5]


def test_compile_context_must_hold_lists():
    with pytest.raises(InvalidContextError):
        DataCompiler().compile({"dragon_id": 1}, CompileContext({"dragons": {"a": 1}}))

    assert DataCompiler().compile({"dragon_id": 1}, CompileContext({"dragons": []})) == {"dragon": None}
    assert DataCompiler().compile({"dragon_id": 1}, CompileContext({"dragons": None})) == {"dragon_id": 1}


def test_custom_suffixes_and_prefixes():
    compiler = DataCompiler(accepted_prefixes=["top_"], ids_suffix="_refs", id_suffix="_ref")

    assert compiler.compile({"top_dragon_refs": [1], "dragon_ref": 2}, context()) == {
        "top_dragons": [{"id": 1, "name": "A"}],
        "dragon": {"id": 2.0, "name": "B"},
    }
    assert compiler.compile({"_ids": [1], "_id": 1}, context()) == {"_ids": [1], "_id": 1}


def test_unknown_id_lists_are_left_alone():
    assert DataCompiler().compile({"island_ids": [1]}, context()) == {"island_ids": [1]}


def test_numeric_coercion_rejects_overflow():
    with pytest.raises(ValueError):
        coerce_number("1e999")
