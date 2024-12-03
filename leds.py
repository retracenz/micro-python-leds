import machine
import neopixel
import time
from config import NUM_LEDS, LED_PIN, RAINBOW, IDLE


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


def mirrorSection(np, colour, secondaryColour, count):
    # Normal Section
    fillSection(np, 0, count, colour)
    fillSection(np, count, int(NUM_LEDS / 2), secondaryColour)
    # Mirror Section
    fillSection(np, int(NUM_LEDS / 2), int(NUM_LEDS) - count, secondaryColour)
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


def wheel(pos):
    """
    Generate rainbow colors across 0-255 positions.
    :param pos: Position in the color wheel (0-255).
    :return: Tuple (R, G, B) for the color.
    """
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)


def rainbowCycle(np, state):
    """
    Cycles through the colours of the rainbow.
    :param np: NeoPixel object.
    :param NUM_LEDS: Number of LEDs in the strip.
    """
    NUM_LEDS = len(np)
    j = 0

    while state["animation_state"] == RAINBOW:
        for i in range(NUM_LEDS):
            np[i] = wheel((i + j) & 255)
        np.write()
        j = (j + 1) % 256

        # Small delay for smooth animation
        time.sleep(0.01)


def stopAnimation(np, state):
    """
    Turns off all LEDs.
    :param np: NeoPixel object.
    :param NUM_LEDS: Number of LEDs in the strip.
    """
    state["animation_state"] = IDLE
    fillColour(np, (0, 0, 0))
