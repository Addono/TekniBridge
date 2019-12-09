from random import randint

from led import Led
from transitions import FadeArray

CHRISTMAS_COLORS = [
    [0.7019607843137254, 0, 0.047058823529411764],
    [0, 0.7019607843137254, 0.17254901960784313],
    [1.0, 0.8431372549019608, 0]
]


class Christmas(FadeArray):
    def __init__(self, rate=0.05):
        super().__init__(rate=rate)

    def step(self, previous):
        if self.targets is None:
            self.targets = [Led(0, 0, 0) for _ in previous]

        if self.converged(previous):
            self.targets = [Led(*CHRISTMAS_COLORS[randint(0, 2)]) for _ in previous]

        return super().step(previous)

    def converged(self, previous):
        for i in range(0, len(previous)):
            if not (self.targets[i].similar(previous[i])):
                return False
        return True
