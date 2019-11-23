import time
from math import exp, log
import os

try:
    from rpi_ws281x import PixelStrip, Color
except ModuleNotFoundError:
    from rpi_ws281x_mock import Color

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


class LedStrip:

    def __init__(self):
        self.pixel_strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.pixel_strip.begin()

    # Define functions which animate LEDs in various ways.
    def color_wipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(startLED):
            self.pixel_strip.setPixelColor(i, Color(0, 0, 0))
        for i in range(startLED, self.pixel_strip.numPixels()):
            self.pixel_strip.setPixelColor(i, color)
            self.pixel_strip.show()
            time.sleep(wait_ms / 1000.0)

    def set_profile(self, profile):
        if profile == "Warm":
            self.color_wipe(self.temp2rgb(1000, 50), 5)
        elif profile == "Cold":
            self.color_wipe(self.temp2rgb(30000, 50), 5)
        elif profile == "OFF":
            self.color_wipe(Color(0, 0, 0), 5)
        elif profile == "WarmStep":
            self.first_order_response(self.temp2rgb(1000, 50),500)
        elif profile == "ColdStep":
            self.first_order_response(self.temp2rgb(30000, 50), 500)

    def first_order_response(self, color, t_millis):
        for i in range(0, t_millis, 10):
            index = 1 - exp(-float(i) / float(t_millis / 5))
            index_led = int(round(index * float(LED_COUNT)))
            for j in range(0, index_led):
                self.pixel_strip.setPixelColor(j, color)
            for j in range(index_led, LED_COUNT):
                self.pixel_strip.setPixelColor(j, Color(0, 0, 0))
            time.sleep(0.01)
            self.pixel_strip.show()

    @staticmethod
    def temp2rgb(temp, brightness=100.0):
        temperature = float(temp) / 100.0
        # red
        if temperature < 66:
            red = 254.0
        else:
            red = (329.6987 * pow(temperature - 60.0, -0.1332))

        # green
        if temperature <= 66:
            green = (99.4708025861 * log(temperature) - 161.1195681661)

        else:
            green = (288.1221695283 * pow(temperature - 60, -0.0755148492))
        # blue
        if temperature > 66:
            blue = 254
        else:
            if temperature <= 19:
                blue = 0
            else:
                blue = (138.5177312231 * log(temperature) - 305.0447927307)

        red *= float(brightness) / 100
        green *= float(brightness) / 100
        blue *= float(brightness) / 100
        print(str(green) + " " + str(red) + " " + str(blue))

        return Color(int(round(red)), int(round(green)), int(round(blue)))
