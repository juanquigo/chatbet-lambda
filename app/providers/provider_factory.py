from .digitain_provider import DigitainProvider


class ProviderFactory:
    _providers = {"digitain": DigitainProvider}

    @staticmethod
    def get_provider(provider):
        provider = ProviderFactory._providers.get(provider)
        if not provider:
            raise ValueError(f"Provider '{provider}' is not supported")
        return provider()
