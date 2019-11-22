import atexit

try:
    xrange(0)
except NameError:
    xrange = range


def Color(red, green, blue, white=0):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return (white << 24) | (red << 16) | (green << 8) | blue


class _LED_Data(object):
    """Wrapper class which makes a SWIG LED color data array look and feel like
    a Python list of integers.
    """

    def __init__(self, size):
        self.size = size
        self.data = [0 for _ in xrange(size)]

    def __getitem__(self, pos):
        """Return the 24-bit RGB color value at the provided position or slice
        of positions.
        """
        # Handle if a slice of positions are passed in by grabbing all the values
        # and returning them in a list.
        if isinstance(pos, slice):
            return [self.data[n] for n in xrange(*pos.indices(self.size))]
        # Else assume the passed in value is a number to the position.
        else:
            return self.data[pos]

    def __setitem__(self, pos, value):
        """Set the 24-bit RGB color value at the provided position or slice of
        positions.
        """
        # Handle if a slice of positions are passed in by setting the appropriate
        # LED data values to the provided values.
        if isinstance(pos, slice):
            index = 0
            for n in xrange(*pos.indices(self.size)):
                self.data[n] = value[index]
                index += 1
        # Else assume the passed in value is a number to the position.
        else:
            self.data[pos] = value
            return value


class PixelStrip(object):
    def __init__(self, num, pin, freq_hz=800000, dma=10, invert=False,
                 brightness=255, channel=0, strip_type=None, gamma=None):
        """Class to represent a SK6812/WS281x LED display.  Num should be the
        number of pixels in the display, and pin should be the GPIO pin connected
        to the display signal line (must be a PWM pin like 18!).  Optional
        parameters are freq, the frequency of the display signal in hertz (default
        800khz), dma, the DMA channel to use (default 10), invert, a boolean
        specifying if the signal line should be inverted (default False), and
        channel, the PWM channel to use (defaults to 0).
        """
        # Grab the led data array.
        self._led_data = _LED_Data(num)

        # Set a has inited flag
        self._is_initialized = False

        self.brightness = brightness

    def setGamma(self, gamma):
        assert self._is_initialized

        if type(gamma) is list and len(gamma) == 256:
            self._gamma = gamma

    def begin(self):
        """Initialize library, must be called once before other functions are
        called.
        """
        self._is_initialized = True

    def show(self):
        """Update the display with the data from the LED buffer."""
        assert self._is_initialized


    def setPixelColor(self, n, color):
        """Set LED at position n to the provided 24-bit color value (in RGB order).
        """
        assert self._is_initialized

        self._led_data[n] = color

    def setPixelColorRGB(self, n, red, green, blue, white=0):
        """Set LED at position n to the provided red, green, and blue color.
        Each color component should be a value from 0 to 255 (where 0 is the
        lowest intensity and 255 is the highest intensity).
        """
        assert self._is_initialized

        self.setPixelColor(n, Color(red, green, blue, white))

    def getBrightness(self):
        assert self._is_initialized

        return self.brightness

    def setBrightness(self, brightness):
        """Scale each LED in the buffer by the provided brightness.  A brightness
        of 0 is the darkest and 255 is the brightest.
        """
        assert self._is_initialized

        self.brightness = brightness

    def getPixels(self):
        """Return an object which allows access to the LED display data as if
        it were a sequence of 24-bit RGB values.
        """
        assert self._is_initialized

        return self._led_data

    def numPixels(self):
        """Return the number of pixels in the display."""
        assert self._is_initialized

        return 100

    def getPixelColor(self, n):
        """Get the 24-bit RGB color value for the LED at position n."""
        assert self._is_initialized

        return self._led_data[n]

    def getPixelColorRGB(self, n):
        assert self._is_initialized

        c = lambda: None

        setattr(c, 'r', self._led_data[n] >> 16 & 0xff)
        setattr(c, 'g', self._led_data[n] >> 8 & 0xff)
        setattr(c, 'b', self._led_data[n] & 0xff)

        return c


# Shim for back-compatibility
class Adafruit_NeoPixel(PixelStrip):
    pass
