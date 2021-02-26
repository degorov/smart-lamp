import network
import utime

apmode = False

def connect(config):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(*config)
        wifi_connect_counter = 0
        wifi_connect_limit = 50
        while not wlan.isconnected():
            wifi_connect_counter = wifi_connect_counter + 1
            if wifi_connect_counter < wifi_connect_limit:
                utime.sleep_ms(100)
            else:
                print('Error while connecting to Wi-Fi')
                return False
    print('Wi-Fi connected:', wlan.ifconfig())
    return True


def hotspot():
    global apmode
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid='Smart-Lamp')
    wlan.active(True)
    apmode = True
    print('Wi-Fi hotspot activated:', wlan.ifconfig())
