import pytest
from app.mappers.mapper_factory import MapperFactory
from app.mappers.digitain_mapper import DigitainMapper


def test_get_mapper_valid():
    mapper = MapperFactory.get_mapper("digitain")
    assert isinstance(mapper, DigitainMapper), "Expected a DigitainMapper instance"


def test_get_mapper_invalid():
    with pytest.raises(ValueError, match="Mapper not found for unknown_provider"):
        MapperFactory.get_mapper("unknown_provider")
