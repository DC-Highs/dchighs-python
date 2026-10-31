import httpx
import pytest


@pytest.fixture
def mock_http(monkeypatch):
    """Makes every ``httpx.AsyncClient()`` created by the library use ``handler`` instead of the network."""
    real_client = httpx.AsyncClient

    def install(handler):
        def factory(**kwargs):
            return real_client(transport=httpx.MockTransport(handler), **kwargs)

        monkeypatch.setattr(httpx, "AsyncClient", factory)

    return install
