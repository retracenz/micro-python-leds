import machine
import neopixel
import time
from config import NUM_LEDS, LED_PIN, RAINBOW, IDLE, RANDOM, XMAS
import random


def initializeLEDs():
    """
    Initializes the NeoPixel strip.
    :return: NeoPixel object.
    """
    return neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)


def fillSection(np, start, stop, colour):
    """
    Sets a section of LEDs to a specific colour.
    :param np: NeoPixel object.
    :param start: Start index of the section.
    :param stop: Stop index of the section.
    :param colour: Tuple (R, G, B) for the colour.
    """
    for i in range(start, stop):
        np[i] = colour
        np.write()


def mirrorSection(np, colour, secondaryColour, count):
    """
    Sets LEDS to a specific colour and mirrors the pattern.
    :param np: NeoPixel object.
    :param colour: Tuple (R, G, B) for the colour.
    :param secondaryColour: Tuple (R, G, B) for the colour.
    :param count: Number of LEDs to fill with the primary colour.
    """
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
    :param state: Dictionary containing the animation state.
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
    :param state: Dictionary containing the animation state.
    """
    state["animation_state"] = IDLE
    fillColour(np, (0, 0, 0))


def xmasLights(np, state):
    """
    Alternates between red and green LEDs.
    :param np: NeoPixel object.
    :param state: Dictionary containing the animation state.
    """
    while state["animation_state"] == XMAS:
        for i in range(NUM_LEDS):
            if i % 2 == 0:
                np[i] = (255, 0, 0)
            else:
                np[i] = (0, 255, 0)
        np.write()

        time.sleep(0.5)

        for i in range(NUM_LEDS):
            if i % 2 == 0:
                np[i] = (0, 255, 0)
            else:
                np[i] = (225, 0, 0)
        np.write()

        time.sleep(0.5)


def randomFlash(np, state):
    """
    Flashes the LEDs with random colors.
    :param np: NeoPixel object.
    :param state: Dictionary containing the animation state.
    """
    while state["animation_state"] == RANDOM:
        for i in range(NUM_LEDS):
            # Generate random RGB values
            np[i] = (random.randint(10, 80), random.randint(
                10, 80), random.randint(10, 80))
        np.write()

        # Small delay to create a flashing effect
        time.sleep(0.1)
