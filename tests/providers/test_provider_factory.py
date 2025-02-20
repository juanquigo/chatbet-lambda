import pytest
from app.providers.provider_factory import ProviderFactory
from app.providers.digitain_provider import DigitainProvider


def test_get_provider_valid():
    provider = ProviderFactory.get_provider("digitain")
    assert isinstance(provider, DigitainProvider)


def test_get_provider_invalid():
    with pytest.raises(ValueError, match="Provider 'None' is not supported"):
        ProviderFactory.get_provider("unknown")
