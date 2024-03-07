import door, limit_switch
import time

import RPi.GPIO as GPIO

GPIO.setwarnings(False)

front_door = door.Door()
#door_limit_switch = limit_switch.LimitSwitch(front_door.door_collision_isr())

def door_operation(action):
    if action == 'open':
        front_door.open_door()
    elif action == 'close':
        front_door.close_door()
    elif action == 'stop':
        front_door.stop_door()
    

front_door.percent_open = 3

try:
    while True:
        door_operation('close')
        time.sleep(5)
        #door_operation('open')
        time.sleep(5)
except:
    door_operation('stop')