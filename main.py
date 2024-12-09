from boot import ledStrip
from leds import mirrorSection, stopAnimation, rainbowCycle, randomFlash, xmasLights
from machine import Pin
from config import BUTTON_PIN, BUTTON_2_PIN, LONG_PRESS_TIME, IDLE, RAINBOW, RANDOM, XMAS
import time

DEBOUNCE_TIME_MS = 50

shared_state = {
    "led_state": False,  # Tracks whether LEDs are on/off
    "button_pressed_time": None,  # Tracks button press time
    "animation_state": IDLE,  # Controls whether to run rainbow cycle
    "animation_number": 0,
    "is_running": False,
}

stopAnimation(ledStrip, shared_state)

green = (0, 25, 5)
blue = (0, 5, 25)
pink = (25, 0, 25)
orange = (45, 25, 0)
red = (25, 0, 0)

# Define the buttons pin (internal pull-up resistor enabled)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
button2 = Pin(BUTTON_2_PIN, Pin.IN, Pin.PULL_UP)


def handleButton(pin, state):
    state["animation_state"] = IDLE

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
    if state['animation_number'] == 4:
        state['animation_number'] = 0

    current_time = time.ticks_ms()

    # Not working... 🤔
    # Ignore rapid successive presses
    if state.get('last_button_event_time') is not None:
        if time.ticks_diff(current_time, state['last_button_event_time']) < DEBOUNCE_TIME_MS:
            return

    state["last_button_event_time"] = current_time

    state["animation_state"] = IDLE

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
                state['animation_state'] = RAINBOW
            else:
                if state['animation_number'] == 0:
                    state['animation_state'] = RANDOM
                    state['animation_number'] += 1
                elif state['animation_number'] == 1:
                    state['animation_state'] = XMAS
                    state['animation_number'] += 1
                else:
                    state['animation_state'] = RAINBOW
                    state['animation_number'] += 1


# Attach interrupt to the button pin
button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
           handler=lambda pin: handleButton(pin, shared_state))

button2.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
            handler=lambda pin: handleButton2(pin, shared_state))

# Keep the program running
try:
    while True:
        # Moved it to here, to try and not block the main loop
        # while shared_state['animation_state'] == RAINBOW and not shared_state["is_running"]:
        while shared_state['animation_state'] == RAINBOW:
            rainbowCycle(ledStrip, shared_state)
        # while shared_state['animation_state'] == RANDOM and not shared_state["is_running"]:
        while shared_state['animation_state'] == RANDOM:
            randomFlash(ledStrip, shared_state)
        # while shared_state['animation_state'] == XMAS and not shared_state["is_running"]:
        while shared_state['animation_state'] == XMAS:
            xmasLights(ledStrip, shared_state)
        else:
            # Sleep briefly to prevent CPU overuse
            time.sleep(0.01)

except KeyboardInterrupt:
    print("Program interrupted.")
    stopAnimation(ledStrip, shared_state)
