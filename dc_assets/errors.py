class AssetsError(Exception):
    """Base class of the errors of this package."""


class AssetsHttpError(AssetsError):
    """The request failed or the server answered with a non-2xx status."""


class InvalidArgumentsError(AssetsError, ValueError):
    """The downloader was built with inconsistent arguments."""
