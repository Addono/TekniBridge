from typing import List

from transitions import Fade
from led import Led

class Wipe(Fade):

    def __init__(self, red: float, green: float, blue: float, rate: float = 0.01) -> None:
        super().__init__(red, green, blue, rate)

        self.index: int = 0

    def step(self, previous: List[Led]) -> List[Led]:
        if (self.index < len(previous)):
            self.index += 1

        # Fade everything below index, freeze everything above it
        return super().step(previous[:self.index]) + previous[self.index:]
