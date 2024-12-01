import network
import time
import machine
import ntptime
import utime
from config import SSID, WIFI_PASSWORD


def get_local_date(offset_hours=0):
    # Get current UTC timestamp
    utc_time = utime.time()
    # Adjust for timezone offset in seconds
    local_time = utc_time + (offset_hours * 3600)
    # Convert back to local time tuple
    local_time_tuple = utime.localtime(local_time)
    year, month, day = local_time_tuple[0], local_time_tuple[1], local_time_tuple[2]
    return year, month, day


def connect_to_wifi():
    """
    Connects to the Wi-Fi network and returns the IP address.
    :return: IP address as a string.
    """
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    # Force the ESP32 to connect to the 2.4 GHz network by specifying the BSSID
    wifi.scan()  # Perform a Wi-Fi scan to get details of all available networks
    for network_info in wifi.scan():
        if network_info[0].decode() == SSID:  # Match the SSID
            # print("Connecting to specific access point...")
            # Use the BSSID of the 2.4 GHz access point
            wifi.connect(SSID, WIFI_PASSWORD, bssid=network_info[1])
            break

    # Wait until connected
    while not wifi.isconnected():
        # print("Connecting...")
        time.sleep(1)

    # print("Connected to Wi-Fi!")
    # print("IP Address:", wifi.ifconfig()[0])
    machine.Pin(2, machine.Pin.OUT).on()  # Turn onboard LED on

    ntptime.host = 'pool.ntp.org'
    ntptime.settime()

    return wifi.ifconfig()[0]
