from led import Led
from transitions import AbstractTransition


class Sudden(AbstractTransition):
    def __init__(self, brightness, red, green, blue):
        self.desired_led = Led(red, green, blue, brightness)

    def step(self, previous):
        return [self.desired_led] * len(previous)
