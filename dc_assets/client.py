import asyncio
from pathlib import Path
from typing import List, Optional, Sequence, Union

import httpx

from dc_assets.errors import AssetsError, AssetsHttpError, InvalidArgumentsError


async def fetch_first(urls: Sequence[str], client: Optional[httpx.AsyncClient] = None) -> bytes:
    """Body of the first URL that answers with a successful status."""
    if not urls:
        raise InvalidArgumentsError("no url to download")

    async def attempt(http: httpx.AsyncClient) -> bytes:
        last_error: Optional[httpx.HTTPError] = None

        for url in urls:
            try:
                response = await http.get(url)
                response.raise_for_status()
                return response.content
            except httpx.HTTPError as error:
                last_error = error

        raise AssetsHttpError(f"http error: {last_error}") from last_error

    if client is not None:
        return await attempt(client)

    async with httpx.AsyncClient(follow_redirects=True) as own_client:
        return await attempt(own_client)


class AssetDownloader:
    """Anything that points to a downloadable file.

    ``urls`` lists the candidates in order: the first one that answers with a successful status wins.
    Pass your own ``httpx.AsyncClient`` (proxies, timeouts, ...) through the ``client`` argument.
    """

    @property
    def url(self) -> str:
        """Primary URL of the file."""
        raise NotImplementedError

    @property
    def urls(self) -> List[str]:
        return [self.url]

    async def fetch(self, client: Optional[httpx.AsyncClient] = None) -> bytes:
        """Downloads the file into memory."""
        return await fetch_first(self.urls, client)

    async def download(
        self,
        path: Union[str, "Path"],
        client: Optional[httpx.AsyncClient] = None,
    ) -> Path:
        """Downloads the file to ``path`` and returns that path."""
        content = await self.fetch(client)
        target = Path(path)

        try:
            await asyncio.get_running_loop().run_in_executor(None, target.write_bytes, content)
        except OSError as error:
            raise AssetsError(f"io error: {error}") from error

        return target
