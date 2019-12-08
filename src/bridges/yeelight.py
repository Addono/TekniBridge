import time
from typing import List

from yeelight import Bulb, BulbException

from bridges import AbstractLight


class Yeelight(AbstractLight):
    def __init__(self, ip: str, supports: List[str]) -> None:
        super().__init__(1)

        self.bulb = Bulb(ip)
        self.bulb.effect = "smooth"
        self.bulb.duration = 1000
        self.bulb.turn_on()

        self.supports: List[str] = supports

        self.previous_rgb: List[int] = [0, 0, 0]
        self.previous_brightness: int = 0
        self.previous_message: int = 0  # Tracks the last time we send a message, used for rate limiting

    def write(self):
        now = time.time()
        backoff = now < self.previous_message + 1  # Set backoff to true when we send a message in the last second.

        [red, green, blue, brightness] = self.leds[0]

        try:
            brightness = 100 * brightness
            # Prevent updating brightness when it either didn't change or we're backing off
            if not backoff and self.previous_brightness != brightness:
                self.bulb.set_brightness(brightness)
                self.previous_brightness = brightness
                self.previous_message = now

            rgb = [int(255 * c) for c in [red, green, blue]]
            # Prevent updating the color if it either didn't change or we're backing off
            if not backoff and self.previous_rgb != rgb and "set_rgb" in self.supports:
                self.previous_rgb = rgb
                self.bulb.set_rgb(*rgb)
                self.previous_message = now

        except BulbException as e:
            print(e)

    @staticmethod
    def from_discover_bulbs_dict(dict: dict):
        return Yeelight(dict["ip"], dict["capabilities"]["support"])
