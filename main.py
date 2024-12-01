from wifi import connect_to_wifi
from leds import mirrorSection
from boot import ledStrip
from tideapi import fetchData, processData
from config import NUM_LEDS
from servo import setAngle
import time

green = (0, 25, 5)
blue = (0, 5, 25)
pink = (25, 0, 25)

mirrorSection(ledStrip, pink, 6)
# Initialize Wi-Fi
connect_to_wifi()

while True:
    tideData = fetchData()

    tideInfo = processData(tideData)

    # If the tide is outgoing
    if tideInfo[1]:
        mirrorSection(ledStrip, blue, int(NUM_LEDS // 2 * (1 - tideInfo[0])))
        setAngle(180)
    else:
        mirrorSection(ledStrip, green, int(NUM_LEDS // 2 * tideInfo[0]))
        setAngle(0)

    time.sleep(12 * 60)  # Sleep for 15 minutes
