
from math import log
from rpi_ws281x import PixelStrip, Color

def temp2rgb(temp, brightness=100.0):
    temperature = float(temp)/100.0
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
            blue = 0;
        else:
            blue = (138.5177312231 * log(temperature) - 305.0447927307);
    red *= float(brightness)/100
    green *= float(brightness)/100
    blue *= float(brightness)/100
    print(str(green) + " " + str(red) + " "+ str(blue))
    return Color(int(round(green)), int(round(red)), int(round(blue)))

