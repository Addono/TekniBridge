from transitions import Fade


class Wipe(Fade):

    def __init__(self, red: float, green: float, blue: float, rate: float = 0.02) -> None:
        super().__init__(red, green, blue, rate)

        self.index = 0

    def step(self, previous):
        if (self.index < len(previous)):
            self.index += 1

        # Fade everything below index, freeze everything above it
        return super().step(previous[:self.index]) + previous[self.index:]
