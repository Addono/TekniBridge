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
        assert 0.0 <= brightness <= 1.0

        self._brightness = float(brightness)

    @abstractmethod
    def step(self, previous: List[Led]) -> List[Led]:
        pass
