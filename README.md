- install micropython firmware\
- Get your usb device id\ 
```$>ls /dev |grep usb```\
```$>pip install esptool```\
```$>esptool.py --port /dev/ttyUSB0 erase_flash``` *change /dev/(your usb device)\
- Download latest firmware https://micropython.org/download/esp32/
```$>esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20170108-v1.8.7.bin```\
- Clone directory
- Fork this repo
- create secret.py inside app directory
```WIFI_SSID='***'```\
```WIFI_PASSWORD='***'```\
```GITREPO='MyNewRepo'```\
```$>git clone MyNewRepo```\
```pip install rshell```\
```$>rshell --buffer-size 30 -p /dev/tty.USB0```\
```$>cp main.py boot.py and app \pyboard```
--tag a release (else it won't work)
- restart you esp and it should start blinking
- If the gods are on your side the code in start.py will execute and you can start building your project out from there.
When your esp32 starts up it will check git for updates and run whatever is in the start.py 
