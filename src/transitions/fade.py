from led import Led
from transitions import AbstractTransition


class Fade(AbstractTransition):
    def __init__(self, brightness, red, green, blue, rate=0.01):
        self.target = Led(red, green, blue, brightness)
        self.rate = rate

    def step(self, previous):
        return [led.blend(self.target, self.rate) for led in previous]
