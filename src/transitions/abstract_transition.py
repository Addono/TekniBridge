from abc import ABCMeta, abstractmethod
from typing import Iterable

from led import Led


class AbstractTransition:
    __metaclass__ = ABCMeta

    @abstractmethod
    def step(self, previous):
        """
        :type previous: Iterable[Led]
        :rtype: list(LED)
        """
        pass