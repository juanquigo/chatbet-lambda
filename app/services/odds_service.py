from app.mappers.mapper_factory import MapperFactory
from app.providers.provider_factory import ProviderFactory


async def get_odds(provider: str, **params: dict[str]) -> dict[str]:
    """Fetch odds from a specified provider and maps the raw data to a standardized format.

    Args:
        provider (str): The name of the provider to fetch odds from.
        **params (dict[str]): Additional parameters to pass to the provider's get_odds method.

    Returns:
        dict[str]: A dictionary containing the mapped odds data.

    """
    provider_instance = ProviderFactory.get_provider(provider=provider)
    raw_data = await provider_instance.get_odds(**params)
    mapper_instance = MapperFactory.get_mapper(provider=provider)
    return mapper_instance.map_odds(raw_data)
