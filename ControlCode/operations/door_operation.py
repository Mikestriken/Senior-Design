import multiprocessing
import json
import sys

from classes import ultrasonic, door, limit_switch, mqtt_connection, motor_current

import RPi.GPIO as GPIO # or gpio setup
GPIO.setwarnings(False)

# * ------------------------------Door Operation-----------------------------------
percent_publisher = mqtt_connection.MQTT_Connection("publisher")

front_door = door.Door()
door_ultrasonic = ultrasonic.Ultrasonic() # y axis detect

threads = []
exit_event = multiprocessing.Event()

def door_operation(action):
    global exit_event
    global threads
    if action == 'open':
        door_operation('stop')

        open_thread = multiprocessing.Process(target=front_door.open_door_multithreading, args=(exit_event, percent_publisher))
        open_thread.start()
        threads.append(open_thread)
    elif action == 'close':
        door_operation('stop') 

        close_thread = multiprocessing.Process(target=front_door.close_door_multithreading, args=(exit_event, percent_publisher))
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
        mqtt_connect.publish("door", str(front_door.percent_open))
    else:
        print('Invalid action posted to topic: door ' + str(action))

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
CURRENT_COUNT = 0

def current_isr(temp_arg):
    global CURRENT_COUNT
    
    if CURRENT_COUNT > 3:
        print("isr called for collision - current")
        door_operation('stop')
        CURRENT_COUNT = 0
    else:
        CURRENT_COUNT += 1

current_detect = motor_current.MotorCurrent(isr=current_isr)

# * ------------------------------Ultrasonic-----------------------------------

def operation_loop():
    while True:
        a=1
        """ reading = door_ultrasonic.get_average_distance(20)
        if reading < 35:
            if front_door.get_percent_open() < 1:
                #door_operation('stop')
                #mqtt_connect.publish('alert', 'Object Blocking Door')
                print('stopped from ultrasonic, reading: ' + str(reading) + 'cm')

            if front_door.get_percent_open() > 60:
                #door_operation('stop')
                #mqtt_connect.publish('alert', 'Object Blocking Door')
                print('stopped from ultrasonic, reading: ' + str(reading) + 'cm') """

operation_loop()

