from classes import fan
import time

fan = fan.Fan()

while True:
    fan.power_on()
    time.sleep(10)
    fan.speed_low()
    time.sleep(6)
    fan.power_off()
    time.sleep(10)