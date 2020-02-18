from abc import ABCMeta, abstractmethod
from typing import Union, List

from led import Led


class AbstractTransition:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self._brightness = 1.0

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness: Union[float, int]):
        # Cast to float
        brightness = float(brightness)

        # Make sure that it is within the range [0, 1]
        assert 0.0 <= brightness <= 1.0

        self._brightness = brightness

    @abstractmethod
    def step(self, previous: List[Led]) -> List[Led]:
        pass
