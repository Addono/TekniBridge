from abc import ABCMeta, abstractmethod


class AbstractTransition:
    __metaclass__ = ABCMeta

    @abstractmethod
    def step(self, previous):
        """
        :type previous: Iterable[Led]
        :rtype: Iterable[Led]
        """
        pass