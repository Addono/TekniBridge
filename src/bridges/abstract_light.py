from abc import ABC, abstractmethod

from led import Led
from transitions import Sudden


class AbstractLight(ABC):
    """
    Abstract representation of a light, represented as a sequence (strip) of LEDs. A single light is the specific case
    when the length of this LED strip is one.
    """

    def __init__(self, led_count: int = 1) -> None:
        super().__init__()

        self.leds = [Led(1.0, 1.0, 1.0) for _ in range(led_count)]
        self.transition = Sudden(0.0, 0.0, 0.0)

    def control(self):
        """
        Updates the value of the LEDs.
        """
        # Take a step
        self.leds = self.transition.step(previous=self.leds)

        # Update the physical LED states
        self.write()

    @abstractmethod
    def write(self):
        """
        Writes the value of the LEDs to the physical device.
        """
        pass
