# boot.py -- run on boot-up
from leds import initialize_leds, stop_animation

ledStrip = initialize_leds()

if __name__ == "__main__":
    stop_animation(ledStrip)  # turn off the LEDs to start
