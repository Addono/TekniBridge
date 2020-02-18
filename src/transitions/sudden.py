from typing import List

from led import Led
from transitions import AbstractTransition


class Sudden(AbstractTransition):

    def __init__(self, red: float, green: float, blue: float) -> None:
        super().__init__()

        self.target = Led(red, green, blue)

    @AbstractTransition.brightness.setter
    def brightness(self, brightness):
        self.target.brightness = brightness
        AbstractTransition.brightness.fset(self, brightness)

    def step(self, previous: List[Led]) -> List[Led]:
        return [self.target for _ in previous]
