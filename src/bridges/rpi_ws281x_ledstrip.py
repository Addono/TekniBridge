import os

from bridges.abstract_light import AbstractLight

try:
    from rpi_ws281x import PixelStrip
except ModuleNotFoundError:
    if os.environ.get('SIMULATE', False):
        print("simulation enabled")
        from rpi_ws281x_mock import VisualPixelStrip as PixelStrip
    else:
        from rpi_ws281x_mock import PixelStrip

# LED strip configuration:
LED_COUNT = 256  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
startLED = 28


class RpiWs281xLedstrip(AbstractLight):

    def __init__(self) -> None:
        super().__init__(led_count=LED_COUNT)
        self.pixel_strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.pixel_strip.begin()

    def write(self):
        assert self.pixel_strip.numPixels() == len(self.leds)

        # Update the value for each of the pixels in the strip
        for i in range(startLED, self.pixel_strip.numPixels()):
            [red, green, blue, brightness] = self.leds[i]
            colors = (int(c * brightness * 255) for c in (red, green, blue))
            self.pixel_strip.setPixelColorRGB(i, *colors, 255)

        # Flush the new values to the strip
        self.pixel_strip.show()
