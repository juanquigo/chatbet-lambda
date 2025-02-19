from abc import ABC, abstractmethod


class BaseMapper(ABC):
    """BaseMapper serves as a blueprint for creating mapper classes that transform.

    Methods:
        map_odds: Abstract method that should be implemented by subclasses
                  to map odds data.

    """

    @abstractmethod
    def map_odds() -> dict[str]:
        """Map odds to a dictionary.

        Returns:
            dict[str]: A dictionary containing the mapped odds.

        """
