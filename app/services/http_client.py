from contextlib import asynccontextmanager

from httpx import AsyncClient


class HTTPClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.client = AsyncClient(base_url=base_url)

    async def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = await self.client.request(method=method.upper(), url=url, **kwargs)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()


@asynccontextmanager
async def get_http_client(base_url: str):
    client = HTTPClient(base_url)
    try:
        yield client
    finally:
        await client.close()
