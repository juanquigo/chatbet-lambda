from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """BaseProvider serves as a blueprint for creating provider classes.

    Methods:
        get_odds: Abstract method that should be implemented by subclasses
                  to get odds data.

    """

    @abstractmethod
    def get_odds() -> dict[str]:
        """Get odds from the provider service.

        Returns:
            dict[str]: The result from the provider service.

        """
