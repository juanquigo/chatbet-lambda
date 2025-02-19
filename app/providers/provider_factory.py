from typing import ClassVar

from app.providers.base_provider import BaseProvider

from .digitain_provider import DigitainProvider


class ProviderFactory:
    _providers: ClassVar[dict[str]] = {"digitain": DigitainProvider}

    @staticmethod
    def get_provider(provider: str) -> BaseProvider:
        """Retrieve an instance of a provider based on the given provider name.

        Args:
            provider (str): The name of the provider to retrieve.

        Returns:
            BaseProvider: An instance of the requested provider.

        Raises:
            ValueError: If the provider name is not supported.

        """
        provider = ProviderFactory._providers.get(provider)
        if not provider:
            error_message = f"Provider '{provider}' is not supported"
            raise ValueError(error_message)
        return provider()
