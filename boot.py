# boot.py -- run on boot-up
import machine
from leds import initialize_leds, stop_animation

ledStrip = initialize_leds()

if __name__ == "__main__":
    machine.Pin(2, machine.Pin.OUT).off()  # Turn onboard LED off

    print("LED strip initialized")
    stop_animation(ledStrip)  # turn off the LEDs to start
    print("LED now turned off!")
