from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from httpx import AsyncClient


class HTTPClient:
    def __init__(self, base_url: str) -> None:
        """Initialize the HTTP client with the given base URL.

        Args:
            base_url (str): The base URL for the HTTP client.

        """
        self.base_url = base_url
        self.client = AsyncClient(base_url=base_url)

    async def request(self, method: str, endpoint: str, **kwargs: dict[str]) -> dict[str]:
        """Send an asynchronous HTTP request using the specified method and endpoint.

        Args:
            method (str): The HTTP method to use for the request (e.g., 'GET', 'POST').
            endpoint (str): The endpoint to send the request to.
            **kwargs (dict[str]): Additional keyword arguments to pass to the request.

        Returns:
            dict[str]: The JSON response from the request.

        Raises:
            HTTPError: If the HTTP request returned an unsuccessful status code.

        """
        url = f"{self.base_url}{endpoint}"
        response = await self.client.request(method=method.upper(), url=url, **kwargs)
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        """Asynchronously closes the HTTP client session.

        This method should be called to properly release any resources held by the
        HTTP client. It ensures that all connections are closed and any pending
        requests are completed.

        Returns:
            None

        """
        await self.client.aclose()


@asynccontextmanager
async def get_http_client(base_url: str) -> AsyncGenerator:
    """Asynchronously creates and yields an HTTP client for the given base URL.

    This function is an asynchronous context manager that yields an instance of
    `HTTPClient` initialized with the provided `base_url`. The client is properly
    closed when the context is exited.

    Args:
        base_url (str): The base URL for the HTTP client.

    Yields:
        AsyncGenerator: An instance of `HTTPClient`.

    Example:
        async with get_http_client("https://api.example.com") as client:
            response = await client.get("/endpoint")
            data = await response.json()

    """
    client = HTTPClient(base_url)
    try:
        yield client
    finally:
        await client.close()
