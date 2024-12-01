import machine
import neopixel
from config import NUM_LEDS, LED_PIN


def initializeLEDs():
    """
    Initializes the NeoPixel strip.
    :param pin: GPIO pin connected to the WS2812B data line.
    :param NUM_LEDS: Number of LEDs in the strip.
    :return: NeoPixel object.
    """
    return neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)


def fillSection(np, start, stop, colour):
    """
    Sets all LEDs to a specific colour.
    :param np: NeoPixel object.
    :param NUM_LEDS: Number of LEDs in the strip.
    :param colour: Tuple (R, G, B) for the colour.
    """
    for i in range(start, stop):
        np[i] = colour
        np.write()


def mirrorSection(np, colour, count):
    # Normal Section
    fillSection(np, 0, count, colour)
    fillSection(np, count, int(NUM_LEDS / 2), (45, 25, 0))
    # Mirror Section
    fillSection(np, int(NUM_LEDS / 2), int(NUM_LEDS) - count, (45, 25, 0))
    fillSection(np, int(NUM_LEDS) - count, int(NUM_LEDS), colour)


def fillColour(np, colour):
    """
    Sets all LEDs to a specific colour.
    :param np: NeoPixel object.
    :param NUM_LEDS: Number of LEDs in the strip.
    :param colour: Tuple (R, G, B) for the colour.
    """
    for i in range(NUM_LEDS):
        np[i] = colour
    np.write()


def stopAnimation(np):
    """
    Turns off all LEDs.
    :param np: NeoPixel object.
    :param NUM_LEDS: Number of LEDs in the strip.
    """
    fillColour(np, (0, 0, 0))
