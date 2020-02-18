from typing import List
from random import randint

from led import Led
from transitions import FadeArray

CHRISTMAS_COLORS = [
    Led(0.7019607843137254, 0, 0.047058823529411764),
    Led(0, 0.7019607843137254, 0.17254901960784313),
    Led(1.0, 0.8431372549019608, 0),
]


class Christmas(FadeArray):
    def __init__(self, rate=0.05):
        super().__init__(rate=rate)

    def step(self, previous: List[Led]) -> List[Led]:
        if self.targets is None:
            self.targets = previous

        if self.converged(previous):
            self.targets = [CHRISTMAS_COLORS[randint(0, 2)] for _ in previous]

        return super().step(previous)

    def converged(self, previous) -> bool:
        for target_led, previous_led in zip(self.targets, previous):
            if not target_led.similar(previous_led, only_color=True):
                return False
        return True
