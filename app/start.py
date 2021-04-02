import network
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

# from machine import Pin
# from time import sleep
#
# led = Pin(2, Pin.OUT)
#
# while True:
#   led.value(not led.value())
#   sleep(0.5)
