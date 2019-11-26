from led import Led
from transitions import AbstractTransition


class Fade(AbstractTransition):
    def __init__(self, red: float, green: float, blue: float, rate: float = 0.01) -> None:
        super().__init__()

        self.target = Led(red, green, blue)
        self.rate = rate

    # @AbstractTransition.brightness.setter
    # def brightness(self, brightness):
    #     super(brightness)
    #     self.target.brightness = brightness

    def step(self, previous):
        self.target.brightness = self.brightness
        return [led.blend(self.target, self.rate) for led in previous]
