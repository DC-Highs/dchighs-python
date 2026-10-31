from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

import httpx

from dc_config.dto import GameConfig, GameData, GameDataConfig
from dc_config.errors import ConfigHttpError
from dc_core import ConfigFilter, ConfigLanguage, ConfigPlatform


@dataclass
class FetchOptions:
    """Fetch the configuration from the authenticated endpoint."""

    url: str
    user_id: str
    auth_token: str = field(repr=False)  # the auth token must never end up in logs
    language: Optional[ConfigLanguage] = None
    platform: Optional[ConfigPlatform] = None
    filter: Optional[Sequence[ConfigFilter]] = None


CreateOptions = FetchOptions


@dataclass
class FetchRawOptions:
    """Fetch a raw (public, unauthenticated) configuration file."""

    url: str
    filter: Optional[Sequence[ConfigFilter]] = None


@dataclass
class CreateRawOptions:
    url: str
    filter: Optional[Sequence[ConfigFilter]] = None
    language: Optional[ConfigLanguage] = None
    platform: Optional[ConfigPlatform] = None


def _join_filter(filter: Sequence[ConfigFilter]) -> str:
    return ",".join(str(item) for item in filter)


def filter_config(full: GameConfig, filter: Optional[Sequence[ConfigFilter]]) -> GameConfig:
    """Keeps only the requested sections that are present (all of them when ``filter`` is empty)."""
    if not filter:
        return full

    sections = full.config.sections
    filtered: Dict[str, Any] = {}

    for key in filter:
        name = str(key)

        if name in sections:
            filtered[name] = sections[name]

    return GameConfig(GameData(GameDataConfig(filtered)))


async def _request(
    client: Optional[httpx.AsyncClient], method: str, url: str, **kwargs: Any
) -> Any:
    try:
        if client is not None:
            response = await client.request(method, url, **kwargs)
        else:
            async with httpx.AsyncClient(follow_redirects=True) as own_client:
                response = await own_client.request(method, url, **kwargs)

        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError) as error:
        raise ConfigHttpError(f"http error: {error}") from error


@dataclass
class Config:
    """A game configuration together with the platform/language/filter it was requested with."""

    data: GameConfig
    platform: ConfigPlatform = ConfigPlatform.IOS
    language: ConfigLanguage = ConfigLanguage.ENGLISH
    filter: Optional[List[ConfigFilter]] = None

    @classmethod
    async def create(
        cls, options: CreateOptions, client: Optional[httpx.AsyncClient] = None
    ) -> "Config":
        """Fetches the configuration from the authenticated endpoint and wraps it."""
        data = await cls.fetch(options, client)

        return cls(
            data=data,
            filter=list(options.filter) if options.filter else None,
            language=options.language or ConfigLanguage.default(),
            platform=options.platform or ConfigPlatform.default(),
        )

    @classmethod
    async def create_raw(
        cls, options: CreateRawOptions, client: Optional[httpx.AsyncClient] = None
    ) -> "Config":
        """Fetches a raw configuration file from a URL and wraps it."""
        data = await cls.fetch_raw(FetchRawOptions(options.url, options.filter), client)

        return cls(
            data=data,
            filter=list(options.filter) if options.filter else None,
            language=options.language or ConfigLanguage.default(),
            platform=options.platform or ConfigPlatform.default(),
        )

    @staticmethod
    async def fetch(options: FetchOptions, client: Optional[httpx.AsyncClient] = None) -> GameConfig:
        """Fetches the configuration from the authenticated endpoint
        (``POST url?authToken=..&userId=..``)."""
        params: Dict[str, str] = {
            "authToken": options.auth_token,
            "userId": options.user_id,
        }

        if options.filter:
            params["filter"] = _join_filter(options.filter)

        if options.platform is not None:
            params["platform"] = str(options.platform)

        if options.language is not None:
            params["language"] = str(options.language)

        body = await _request(client, "POST", options.url, params=params)
        return GameConfig.from_dict(body)

    @staticmethod
    async def fetch_raw(
        options: FetchRawOptions, client: Optional[httpx.AsyncClient] = None
    ) -> GameConfig:
        """Fetches a raw configuration file and keeps only the requested sections
        (all of them when ``filter`` is ``None`` or empty)."""
        body = await _request(client, "GET", options.url)
        return filter_config(GameConfig.from_dict(body), options.filter)
