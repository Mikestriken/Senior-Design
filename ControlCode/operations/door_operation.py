##################################################################################
#                         Door Operation Python Script
# This python script controls the opening and closing of the door based on
# a variety of different sensors such as:
#   - Limit Switches # ! NOTE: NOW OBSOLETE
#   - Ultrasonic Sensor
#   - Door Motor Current Sensor
#   - Receive Signal Strength Indication (RSSI) from a robot connected to the router.
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##################################################################################

import multiprocessing
import json
import sys
import time

from classes import door, limit_switch, mqtt_connection, motor_current

import RPi.GPIO as GPIO # or gpio setup
GPIO.setwarnings(False)

# * ------------------------------Door Operation-----------------------------------
percent_publisher = mqtt_connection.MQTT_Connection("publisher")

front_door = door.Door()

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
        # global CURRENT_COUNT
        
        front_door.stop_door()

        exit_event.set()
        for process in threads:
            process.terminate()
            process.join()
        
        exit_event = multiprocessing.Event()
        threads = []
        # CURRENT_COUNT = 0
        
    elif action == 'query_state':
        mqtt_connect.publish("door", str(front_door.percent_open))
    else:
        print('Invalid action posted to topic: door ' + str(action))

def door_collision_isr():
    door_operation('stop')
    print("collision detected")

#door_limit_switch = limit_switch.LimitSwitch(limit_isr=door_collision_isr)

# * ------------------------------Mqtt Connection-----------------------------------
CURRENT_SENSOR_ENABLED = True

def on_message_main(self, client, msg):
    global CURRENT_SENSOR_ENABLED
    if msg.topic == 'current_sensor' and msg.payload.decode("utf-8") == 'off':
        CURRENT_SENSOR_ENABLED = False
    elif msg.topic == 'current_sensor' and msg.payload.decode("utf-8") == 'on':
        CURRENT_SENSOR_ENABLED = True
    if msg.topic == 'door_request' or msg.topic == "door":
        door_operation(msg.payload.decode("utf-8"))
                  
mqtt_connect = mqtt_connection.MQTT_Connection(type='both', topics = ['door', 'door_request', 'current_sensor'], on_message=on_message_main)

# * ------------------------------Motor Current-----------------------------------
CURRENT_COUNT = 0

def current_isr(temp_arg):
    global CURRENT_COUNT
    global CURRENT_SENSOR_ENABLED

    if CURRENT_SENSOR_ENABLED:
        if CURRENT_COUNT > 4:
            door_operation('stop')
            print("isr called for collision - current")
            mqtt_connect.publish('alerts', 'Object Blocking Door')
            CURRENT_COUNT = 0
        else:
            CURRENT_COUNT += 1

current_detect = motor_current.MotorCurrent(isr=current_isr)

# * ------------------------------Operation Loop---------------------------------

def operation_loop():
    while True:
        time.sleep(.01)
        

operation_loop()

