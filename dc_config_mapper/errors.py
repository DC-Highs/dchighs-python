from typing import Any


class MapperError(Exception):
    """Base class of every error of this package."""


class SchemaError(MapperError):
    """A configuration object did not match the (strict) schema of its mapper."""

    def __init__(self, schema: str, source: Exception) -> None:
        self.schema = schema
        self.source = source
        super().__init__(f"invalid {schema}: {source}")


class MissingFieldError(MapperError):
    """A section is missing a key (or it has the wrong JSON type)."""

    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(f"section is missing the array/object `{key}`")


class RewardNotFoundError(MapperError):
    """A chest references a reward id that does not exist."""

    def __init__(self, reward_id: Any) -> None:
        self.reward_id = reward_id
        super().__init__(f"reward {reward_id} not found")


class InvalidBooleanError(MapperError):
    """A flag that should be ``0`` or ``1`` had another value."""

    def __init__(self, value: Any) -> None:
        self.value = value
        super().__init__(f"invalid number {value}, expected 0 or 1")


class UnexpectedPriceError(MapperError):
    """A ``costs`` object had more than one currency, or an unknown one."""

    def __init__(self, message: str) -> None:
        super().__init__(f"unexpected price: {message}")


class UnprocessedRewardsError(MapperError):
    """A reward object contained something the mapper does not understand."""

    def __init__(self, message: str) -> None:
        super().__init__(f"rewards not processed correctly: {message}")


class InvalidTimestampError(MapperError):
    """A timestamp does not fit in a date."""

    def __init__(self, value: Any) -> None:
        super().__init__(f"invalid timestamp: {value}")


class InvalidNumberError(MapperError):
    """A numeric operation overflowed or produced a non-finite number."""

    def __init__(self, what: str) -> None:
        super().__init__(f"invalid numeric operation on {what}")


class DecorationPositionMismatchError(MapperError):
    """Number of free board positions differs from the number of decorations."""

    def __init__(self) -> None:
        super().__init__("number of decoration positions does not match number of decorations")


class InvalidContextError(MapperError):
    """The compile context entry used to resolve ids is not an array."""

    def __init__(self, name: str) -> None:
        super().__init__(f"compile context entry `{name}` is not an array")


class MaxDepthExceededError(MapperError):
    """The compiled data references itself (or is nested too deep)."""

    def __init__(self, depth: int) -> None:
        super().__init__(f"data compilation exceeded the maximum depth of {depth} (circular reference?)")
