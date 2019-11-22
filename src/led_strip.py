import time

from math import exp

try:
    from rpi_ws281x import PixelStrip, Color
except ModuleNotFoundError:
    from rpi_ws281x_mock import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 250  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
startLED = 28


# Define functions which animate LEDs in various ways.
def color_wipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(startLED):
        strip.setPixelColor(i, Color(0, 0, 0))
    for i in range(startLED, strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def firstOrderResponse(strip, color, T_millis):
    for i in range(0, T_millis, 10):
        index = 1 - exp(-float(i) / float(T_millis/5))
        index_led = int(round(index * float(LED_COUNT)))
        for j in range(0, index_led):
            strip.setPixelColor(j, color)
        for j in range(index_led, LED_COUNT):
            strip.setPixelColor(j, Color(0, 0, 0))
        time.sleep(0.01)
        strip.show()


if __name__ == '__main__':
    # Create the LED strip object
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

    # Initialize the library (must be called once before other functions).
    strip.begin()

    while True:
        for temp in range(1000, 40000, 10):
            color_wipe(strip, temp2rgb(temp, 20), 5)
        #for duration in range(200, 1000, 50):
        #    firstOrderResponse(strip, Color(60, 120, 60), duration)
        #   color_wipe(strip, Color(0,0,0), 5)

"""     void LEDStrip::temperature(float temperature)
{

    temperature /= 100;
    Vec3b rgb;
    if (temperature < 66)
        rgb[0] = 255;
    else
        rgb[0] = (char)(329.6987 * pow(temperature - 60.0, -0.1332));

    if (temperature <= 66)
    {
        rgb[1] = (char)(99.4708025861 * log(temperature) - 161.1195681661);
    }
    else
        rgb[1] = (char)(288.1221695283 * pow(temperature - 60, -0.0755148492));

    if (temperature > 66)
        rgb[2] = 255;
    else
    {
        if (rgb[2] <= 19)
            rgb[2] = 0;
        else
            rgb[2] = (char)(138.5177312231 * log(temperature) - 305.0447927307);
    }

    image1D->setTo(rgb);
}

void LEDStrip::firstOrderResponse(int millisec, Vec3b rgb)
{
    clock_t t1, t2;
    t1 = clock();
    for (int i = 0; i < millisec; i++)
    {
        double index = 1 - exp(-i / millisec);
        image1D->setTo(Scalar(0, 0, 0));
        (*image1D)(cv::Rect(0, 0, (int)index, 1)).setTo(rgb);
        while(!((clock()-t1)/CLOCKS_PER_SEC/1000>i));
        writePixels();
        
    }


} """
