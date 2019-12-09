from random import randint

from led import Led
from transitions import FadeArray

CHRISTMAS_COLORS = [[0.7019607843137254, 0, 0.047058823529411764], [0, 0.7019607843137254, 0.17254901960784313],
                    [1.0, 0.8431372549019608, 0]]


class Christmas(FadeArray):
    def __init__(self, rate=0.05):
        super().__init__(rate=rate)

    def step(self, previous):
        self.fix_dimension(previous)
        index = randint(0, len(previous) - 1)
        self.targets[index] = Led(*CHRISTMAS_COLORS[randint(0, 2)])
        return self.computeFade(previous)
