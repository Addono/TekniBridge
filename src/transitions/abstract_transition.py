from abc import ABCMeta, abstractmethod
from typing import Iterable

from led import Led


class AbstractTransition:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self._brightness = 1.0

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness: float):
        # assert 0.0 <= brightness and brightness <= 1.0

        self._brightness = brightness

    @abstractmethod
    def step(self, previous):
        """
        :type previous: Iterable[Led]
        :rtype: Iterable[Led]
        """
        pass
