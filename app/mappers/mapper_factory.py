from .digitain_mapper import DigitainMapper


class MapperFactory:
    _mappers = {"digitain": DigitainMapper}

    @staticmethod
    def get_mapper(provider):
        mapper_class = MapperFactory._mappers.get(provider)
        if not mapper_class:
            raise ValueError(f"Mapper not found for {provider}")
        return mapper_class()
