from abc import ABC, abstractmethod


class BaseProviderStrategy(ABC):
    def __init__(self, settings):
        self.settings = settings

    @abstractmethod
    async def get_odds(self):
        pass
