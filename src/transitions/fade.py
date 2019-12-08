from led import Led
from transitions import AbstractTransition


class Fade(AbstractTransition):

    def __init__(self, red: float, green: float, blue: float, rate: float = 0.02) -> None:
        super().__init__()

        self.target = Led(red, green, blue)
        self.rate = rate

    @AbstractTransition.brightness.setter
    def brightness(self, brightness):
        self.target.brightness = brightness
        AbstractTransition.brightness.fset(self, brightness)

    def step(self, previous):
        return [led.blend(self.target, self.rate) for led in previous]
