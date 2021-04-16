def connectToWifiAndUpdate():
    import time, machine, network, gc, app.secrets as secrets
    from app.mp_i2c_lcd1602 import LCD1602
    from machine import I2C, Pin
    time.sleep(1)
    print('Memory free', gc.mem_free())

    i2c = I2C(1, sda=Pin(22), scl=Pin(23))
    LCD = LCD1602(i2c, i2c.scan()[0])
    from app.ota_updater import OTAUpdater

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        LCD.puts("connecting to network...")
        sta_if.active(True)
        sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    LCD.puts('network config:', sta_if.ifconfig())
    otaUpdater = OTAUpdater(secrets.GITREPO, main_dir='app', secrets_file="secrets.py")
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        LCD.puts('Resetting....')
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()

def startApp():
    import app.start


connectToWifiAndUpdate()
startApp()
