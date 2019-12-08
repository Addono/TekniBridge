from led import Led
from transitions import AbstractTransition


class Wipe(AbstractTransition):

    def __init__(self, red: float, green: float, blue: float, rate: float = 0.9) -> None:
        super().__init__()
        self.index = 0
        self.target = Led(red, green, blue)
        self.rate = rate

    @AbstractTransition.brightness.setter
    def brightness(self, brightness):
        self.target.brightness = brightness
        AbstractTransition.brightness.fset(brightness)

    def step(self, previous):

        previous[self.index] = previous[self.index].blend(self.target, self.rate)
        if previous[self.index].similar(self.target) and self.index < len(previous)-1:
            previous[self.index] = self.target
            self.index += 1
        return previous
