import machine
import neopixel
import time
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


def rainbowCycle(np):
    """
    Cycles through the colours of the rainbow.
    :param np: NeoPixel object.
    :param NUM_LEDS: Number of LEDs in the strip.
    """
    for j in range(255):
        for i in range(NUM_LEDS):
            np[i] = wheel((i + j) & 255)
        np.write()

        # Check if button2 is pressed
        # if button2.value() == 0:  # Button is pressed
        #     print("Button pressed! Exiting rainbowCycle.")
        #     return  # Exit the function

        time.sleep(0.1)


def stopAnimation(np):
    """
    Turns off all LEDs.
    :param np: NeoPixel object.
    :param NUM_LEDS: Number of LEDs in the strip.
    """
    fillColour(np, (0, 0, 0))
