import multiprocessing
import json
import sys

from classes import ultrasonic, door, limit_switch, mqtt_connection, motor_current

import RPi.GPIO as GPIO # or gpio setup
GPIO.setwarnings(False)

# * ------------------------------Door Operation-----------------------------------

front_door = door.Door()
door_ultrasonic = ultrasonic.Ultrasonic() # y axis detect

threads = []
exit_event = multiprocessing.Event()

def door_operation(action):
    global exit_event
    global threads
    if action == 'open':
        open_thread = multiprocessing.Process(target=front_door.open_door_multithreading, args=(exit_event,))
        open_thread.start()
        threads.append(open_thread)
    elif action == 'close':
        close_thread = multiprocessing.Process(target=front_door.close_door_multithreading, args=(exit_event,))
        close_thread.start()
        threads.append(close_thread)
    elif action == 'stop':
        front_door.stop_door()

        exit_event.set()
        for process in threads:
            process.terminate()
            process.join()
        
        exit_event = multiprocessing.Event()
        threads = []
    elif action == 'query_state':
        mqtt_connect.publish('door', str(front_door.percent_open))
    else:
        print('Invalid action posted to topic: door' + str(action))

def door_collision_isr():
        door_operation('stop')
        print("collision detected")

#door_limit_switch = limit_switch.LimitSwitch(limit_isr=door_collision_isr)

# * ------------------------------Mqtt Connection-----------------------------------

def on_message_main(self, client, msg):
    
    if msg.topic == 'door_request' or msg.topic == "door":
        door_operation(msg.payload.decode("utf-8"))
                  
mqtt_connect = mqtt_connection.MQTT_Connection(type='both', topics = ['door', 'door_request'], on_message=on_message_main)

# * ------------------------------Motor Current-----------------------------------
def isr():
    door_operation('stop')

current_detect = motor_current.MotorCurrent(isr=isr)

# * ------------------------------Ultrasonic-----------------------------------

def ultrasonic_operation():
    while True:
        reading = door_ultrasonic.get_average_distance(20)
        if reading < 35:
            if front_door.get_percent_open() < 1:
                door_operation('stop')
                mqtt_connect.publish('alert', 'Object Blocking Door')
                print('stopped from ultrasonic, reading: ' + str(reading) + 'cm')

            if front_door.get_percent_open() > 60:
                door_operation('stop')
                mqtt_connect.publishAsJSON('alert', 'Object Blocking Door')
                print('stopped from ultrasonic, reading: ' + str(reading) + 'cm')

ultrasonic_operation()

