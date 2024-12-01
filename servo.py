from machine import Pin, PWM
import time
from config import SERVO_PIN

# Initialize PWM on GPIO 15 (adjust if using a different pin)
servo = PWM(Pin(SERVO_PIN), freq=50)  # 50 Hz for servos


def setAngle(angle):
    # Convert angle (0-180 degrees) to duty cycle (500-2500 microseconds)
    duty = int(((angle) / 180.0 * 2000) + 500)
    servo.duty_u16(duty * 65536 // 20000)  # Scale to 16-bit (0-65535)
    time.sleep(0.5)  # Allow time for the servo to move
