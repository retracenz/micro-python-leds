from boot import ledStrip
from leds import mirrorSection, stopAnimation, rainbowCycle
from machine import Pin
from config import BUTTON_PIN, BUTTON_2_PIN, LONG_PRESS_TIME
import time
import random

shared_state = {
    "led_state": False,  # Tracks whether LEDs are on/off
    "button_pressed_time": None,  # Tracks button press time
    "stop_flag": False,  # Controls whether animations should stop
}

stopAnimation(ledStrip, shared_state)

green = (0, 25, 5)
blue = (0, 5, 25)
pink = (25, 0, 25)
orange = (45, 25, 0)

# Define the buttons pin (internal pull-up resistor enabled)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
button2 = Pin(BUTTON_2_PIN, Pin.IN, Pin.PULL_UP)


def handleButton(pin, state):

    if not pin.value():  # Button pressed (active low)
        # Record the time when the button was first pressed
        if state['button_pressed_time'] is None:
            state['button_pressed_time'] = time.ticks_ms()
    else:  # Button released
        if state['button_pressed_time'] is not None:
            press_duration = time.ticks_diff(
                time.ticks_ms(), state['button_pressed_time']) / 1000.0
            state['button_pressed_time'] = None  # Reset the pressed time

            if press_duration > LONG_PRESS_TIME:
                # Long press detected: turn off LEDs completely
                stopAnimation(ledStrip, state)
            else:
                # Short press detected: toggle LEDs
                state['led_state'] = not state['led_state']

                if state['led_state']:
                    mirrorSection(ledStrip, pink, green, 20)
                else:
                    mirrorSection(ledStrip, blue, orange, 50)


def handleButton2(pin, state):
    state["stop_flag"] = True

    if not pin.value():  # Button pressed (active low)
        # Record the time when the button was first pressed
        if state['button_pressed_time'] is None:
            state['button_pressed_time'] = time.ticks_ms()
    else:  # Button released
        if state['button_pressed_time'] is not None:
            press_duration = time.ticks_diff(
                time.ticks_ms(), state['button_pressed_time']) / 1000.0
            state['button_pressed_time'] = None  # Reset the pressed time

            if press_duration > LONG_PRESS_TIME:
                # Long press detected: rainbow cycle!! 🌈
                state["stop_flag"] = False  # Reset stop flag
                rainbowCycle(ledStrip, state)
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
button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
           handler=lambda pin: handleButton(pin, shared_state))

button2.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
            handler=lambda pin: handleButton2(pin, shared_state))

# Keep the program running
try:
    while True:
        pass

except KeyboardInterrupt:
    print("Program interrupted.")
    stopAnimation(ledStrip, shared_state)
