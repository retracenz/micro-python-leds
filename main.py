from boot import ledStrip
from leds import mirrorSection, stopAnimation, rainbowCycle
from machine import Pin
from config import BUTTON_PIN, BUTTON_2_PIN
import time
import random

stopAnimation(ledStrip)

green = (0, 25, 5)
blue = (0, 5, 25)
pink = (25, 0, 25)
orange = (45, 25, 0)

# Define the buttons pin (internal pull-up resistor enabled)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
button2 = Pin(BUTTON_2_PIN, Pin.IN, Pin.PULL_UP)

# Variables to track state
led_state = False
long_press_time = 1  # Time in seconds to detect a long press
button_pressed_time = None


def handleButton(pin):
    global led_state, button_pressed_time

    if not pin.value():  # Button pressed (active low)
        # Record the time when the button was first pressed
        if button_pressed_time is None:
            button_pressed_time = time.ticks_ms()
    else:  # Button released
        if button_pressed_time is not None:
            press_duration = time.ticks_diff(
                time.ticks_ms(), button_pressed_time) / 1000.0
            button_pressed_time = None  # Reset the pressed time

            if press_duration > long_press_time:
                # Long press detected: turn off LEDs completely
                stopAnimation(ledStrip)
            else:
                # Short press detected: toggle LEDs
                led_state = not led_state

                if led_state:
                    mirrorSection(ledStrip, pink, green, 20)
                else:
                    mirrorSection(ledStrip, blue, orange, 50)


def handleButton2(pin):
    global led_state, button_pressed_time

    if not pin.value():  # Button pressed (active low)
        # Record the time when the button was first pressed
        if button_pressed_time is None:
            button_pressed_time = time.ticks_ms()
    else:  # Button released
        if button_pressed_time is not None:
            press_duration = time.ticks_diff(
                time.ticks_ms(), button_pressed_time) / 1000.0
            button_pressed_time = None  # Reset the pressed time

            if press_duration > long_press_time:
                # Long press detected: turn off LEDs completely
                rainbowCycle(ledStrip)
            else:
                mirrorSection(
                    ledStrip,
                    (random.randint(1, 255), random.randint(
                        1, 255), random.randint(1, 255)),
                    (random.randint(1, 255), random.randint(
                        1, 255), random.randint(1, 255)),
                    random.randint(1, 60)
                )


# Attach interrupt to the button pin
button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=handleButton)

button2.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=handleButton2)

# Keep the program running
try:
    while True:
        pass

except KeyboardInterrupt:
    print("Program interrupted.")
    stopAnimation(ledStrip)
