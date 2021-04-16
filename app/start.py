try:
  import usocket as socket
except:
  import socket

from app.mp_i2c_lcd1602 import LCD1602
from time import sleep_ms
from machine import I2C, Pin
import network
import app.secrets

import esp
esp.osdebug(None)

import gc
gc.collect()
i2c = I2C(1, sda=Pin(22), scl=Pin(23))
LCD = LCD1602(i2c, i2c.scan()[0])

ssid = app.secrets.WIFI_SSID
password = app.secrets.WIFI_PASSWORD

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)
LCD.puts("App started!")
sleep_ms(10000)

while station.isconnected() == False:
  pass

LCD.puts("Connection successful")
sleep_ms(10000)
print('Connection successful')
LCD.puts(station.ifconfig())
sleep_ms(10000)
print(station.ifconfig())

# ESP32 GPIO 26
relay = Pin(2, Pin.OUT)



def web_page():
  if relay.value() == 1:
    relay_state = ''
  else:
    relay_state = 'checked'
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>
  body{font-family:Arial; text-align: center; margin: 0px auto; padding-top:30px;}
  .switch{position:relative;display:inline-block;width:120px;height:68px}.switch input{display:none}
  .slider{position:absolute;top:0;left:0;right:0;bottom:0;background-color:#ccc;border-radius:34px}
  .slider:before{position:absolute;content:"";height:52px;width:52px;left:8px;bottom:8px;background-color:#fff;-webkit-transition:.4s;transition:.4s;border-radius:68px}
  input:checked+.slider{background-color:#2196F3}
  input:checked+.slider:before{-webkit-transform:translateX(52px);-ms-transform:translateX(52px);transform:translateX(52px)}
  </style><script>function toggleCheckbox(element) { var xhr = new XMLHttpRequest(); if(element.checked){ xhr.open("GET", "/?relay=on", true); }
  else { xhr.open("GET", "/?relay=off", true); } xhr.send(); }</script></head><body>
  <h1>ESP Relay Web Server</h1><label class="switch"><input type="checkbox" onchange="toggleCheckbox(this)" %s><span class="slider">
  </span></label></body></html>""" % (relay_state)
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    relay_on = request.find('/?relay=on')
    relay_off = request.find('/?relay=off')
    if relay_on == 6:
      print('RELAY ON')
      relay.value(0)
    if relay_off == 6:
      print('RELAY OFF')
      relay.value(1)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')

n = 0
while 1:
    LCD.puts(n, 0, 1)
    n += 1
    sleep_ms(1000)
