import _thread as th
from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)
blink_running = True

def blink(delay):
     while blink_running:
         led.value(not led.value())
         time.sleep(delay)
         led.value(0)


print("Starting other tasks...")
th.start_new_thread(blink, (0.5))

count = 0
while True:
  print("Doing stuff... " + str(count))
  count += 1
  if count >= 10:
    break
  time.sleep(1)

print("Ending threads...")
#blink_running = False
