import machine
import neopixel
from config import NUM_LEDS, LED_PIN


def initialize_leds():
    """
    Initializes the NeoPixel strip.
    :param pin: GPIO pin connected to the WS2812B data line.
    :param NUM_LEDS: Number of LEDs in the strip.
    :return: NeoPixel object.
    """
    return neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)


def fillSection(np, start, stop, color):
    """
    Sets all LEDs to a specific color.
    :param np: NeoPixel object.
    :param NUM_LEDS: Number of LEDs in the strip.
    :param color: Tuple (R, G, B) for the color.
    """
    for i in range(start, stop):
        np[i] = color
        np.write()


def mirrorSection(np, colour, count):
    # Normal Section
    fillSection(np, 0, count, colour)
    fillSection(np, count, int(NUM_LEDS / 2), (45, 25, 0))
    # Mirror Section
    fillSection(np, int(NUM_LEDS / 2), int(NUM_LEDS) - count, (45, 25, 0))
    fillSection(np, int(NUM_LEDS) - count, int(NUM_LEDS), colour)


def fill_color(np, color):
    """
    Sets all LEDs to a specific color.
    :param np: NeoPixel object.
    :param NUM_LEDS: Number of LEDs in the strip.
    :param color: Tuple (R, G, B) for the color.
    """
    for i in range(NUM_LEDS):
        np[i] = color
    np.write()


def stop_animation(np):
    """
    Turns off all LEDs.
    :param np: NeoPixel object.
    :param NUM_LEDS: Number of LEDs in the strip.
    """
    fill_color(np, (0, 0, 0))
    print("Animation stopped and LEDs turned off.")
