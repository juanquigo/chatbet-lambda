from typing import ClassVar

from .digitain_mapper import DigitainMapper


class MapperFactory:
    _mappers: ClassVar[dict[str]] = {"digitain": DigitainMapper}

    @staticmethod
    def get_mapper(provider: str) -> object:
        """Retrieve the mapper class instance for the given provider.

        Args:
            provider (str): The name of the provider for which to get the mapper.

        Returns:
            object: An instance of the mapper class corresponding to the given provider.

        Raises:
            ValueError: If no mapper class is found for the given provider.

        """
        mapper_class = MapperFactory._mappers.get(provider)
        if not mapper_class:
            error_message = f"Mapper not found for {provider}"
            raise ValueError(error_message)
        return mapper_class()
