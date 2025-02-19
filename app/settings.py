from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Provider(BaseModel):
    base_url: str


class Settings(BaseSettings):
    app_name: str
    providers: dict[str, Provider]
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")


@lru_cache
def get_settings():
    return Settings().model_dump()
