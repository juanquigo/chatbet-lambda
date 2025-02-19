from app.mappers.mapper_factory import MapperFactory
from app.providers.provider_factory import ProviderFactory


async def get_odds(provider, **params):
    provider_instance = ProviderFactory.get_provider(provider=provider)
    raw_data = await provider_instance.get_odds(**params)
    mapper_instance = MapperFactory.get_mapper(provider=provider)
    return mapper_instance.map_odds(raw_data)
