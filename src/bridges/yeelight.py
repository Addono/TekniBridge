import time
from typing import List

from yeelight import Bulb, BulbException

from bridges import AbstractLight


class Yeelight(AbstractLight):
    def __init__(self, ip: str, supports: List[str]) -> None:
        """
        @type ip: The ip of the light bulb
        @type supports: A list of all methods this light bulb supports
        """
        super().__init__(1)

        self.bulb = Bulb(ip)
        self.bulb.effect = "smooth"
        self.bulb.duration = 1000
        self.bulb.turn_on()

        self.supports = supports

        properties = self.bulb.get_properties()

        # We could also parse rgb from properties, however the encoding does not seem trivial.
        self.previous_rgb = [0, 0, 0]
        self.previous_brightness = float(properties["current_brightness"]) / 100  # Scale from [0, 100] to [0, 1]
        self.previous_power = properties["power"]

        self.next_message = 0  # Tracks the last time we send a message, used for rate limiting

    def write(self):
        # Check if we should back off
        if time.time() < self.next_message:
            return

        [red, green, blue, brightness] = self.leds[0]  # Get the desired light state values.
        send_messages_count = 0  # Track the amount of messages we send during this write.

        try:
            # Only update the brightness if the difference is more than one percent
            if abs(self.previous_brightness - brightness) > 0.01:
                # Turn the light off when brightness approaches zero and it is turned on
                if brightness < 0.01 and self.previous_power == "on":
                    self.bulb.turn_off()
                    self.previous_power = "off"
                    send_messages_count += 1
                else:
                    # Turn the light off in case it was previously turned off
                    if self.previous_power == "off":
                        self.bulb.turn_on()
                        self.previous_power = "on"
                        send_messages_count += 1

                    # Update the brightness
                    self.bulb.set_brightness(brightness * 100)  # Scale from [0, 1] to [0, 100]
                    self.previous_brightness = brightness
                    send_messages_count += 1

            rgb = [int(255 * c) for c in [red, green, blue]]
            # Prevent updating the color if it either didn't change or we're backing off
            if self.previous_rgb != rgb and "set_rgb" in self.supports:
                self.previous_rgb = rgb
                self.bulb.set_rgb(*rgb)
                send_messages_count += 1
        except BulbException as e:
            print(e)
        finally:
            # Make sure we back off for #send_messages seconds to prevent hitting the rate limiting cap.
            if send_messages_count > 0:
                self.next_message = time.time() + send_messages_count

    @staticmethod
    def from_discover_bulbs_dict(dict: dict):
        return Yeelight(dict["ip"], dict["capabilities"]["support"])
