
from math import log
from rpi_ws281x import PixelStrip, Color

def temp2rgb(temperature):
    temperature/=100
    # red
    if temperature < 66:
        red = 255
    else:
        red = (329.6987 * pow(temperature - 60.0, -0.1332))

    # green
    if temperature <= 66:
        green = (99.4708025861 * log(temperature) - 161.1195681661)

    else:
        green = (288.1221695283 * pow(temperature - 60, -0.0755148492))
    # blue
    if temperature > 66:
        blue = 255
    else:
        if temperature <= 19:
            blue = 0;
        else:
            blue = (138.5177312231 * log(temperature) - 305.0447927307);
    return Color(int(round(green)), int(round(red)), int(round(blue)))
"""
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
"""