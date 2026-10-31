class ConfigError(Exception):
    """Base class of the errors of this package."""


class ConfigHttpError(ConfigError):
    """The request failed, the server answered with a non-2xx status or the body was not the expected JSON."""
