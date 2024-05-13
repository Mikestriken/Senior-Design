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
# Commented by Michael Marais for EPRI_SPOT, Spring 2024
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

# * This function classifies requests on the MQTT topic door_request to open / close / stop the door.
# * The function is also called directly by an ISR for GPIO 18 defined below. This GPIO 18 ISR is triggered by the current sensor when
# * the motor attempts to draw too much current when an obstacle blocks the door.
def door_operation(action):
    global exit_event
    global threads
    
    # * To open the door:
    if action == 'open':
        # * 1. Stop the door
        door_operation('stop')

        # * 2. Start opening the door by instantiating a new thread that opens the door and keeps track of the door's progress via a timer based % open.
        open_thread = multiprocessing.Process(target=front_door.open_door_multithreading, args=(exit_event, percent_publisher))
        open_thread.start()
        threads.append(open_thread)
        
    # * To close the door:
    elif action == 'close':
        # * 1. Stop the door
        door_operation('stop') 

        # * 2. Start closing the door by instantiating a new thread that closes the door and keeps track of the door's progress via a timer based % close.
        close_thread = multiprocessing.Process(target=front_door.close_door_multithreading, args=(exit_event, percent_publisher))
        close_thread.start()
        threads.append(close_thread)
        
    # * To stop the door:
    elif action == 'stop':
        # global CURRENT_COUNT
        
        # * 1. Set the DC Motor driver pins to a brake configuration
        front_door.stop_door()

        # * 2. Stop any background threads that are currently incrementing / decrementing the % open to keep track of the door's progress.
        exit_event.set()
        for process in threads:
            process.terminate()
            process.join()
        
        exit_event = multiprocessing.Event()
        threads = []
        
        # * 3. Reset the current spike counter.
        CURRENT_COUNT = 0
        
    # * If the door's current % open is requested, publish it to the 'door' MQTT topic.
    elif action == 'query_state':
        mqtt_connect.publish("door", str(front_door.percent_open))
    else:
        print('Invalid action posted to topic: door ' + str(action))

# * Appears to be legacy code that does nothing -- Michael
def door_collision_isr():
    door_operation('stop')
    print("collision detected")

#door_limit_switch = limit_switch.LimitSwitch(limit_isr=door_collision_isr)

# * ------------------------------Mqtt Connection-----------------------------------
CURRENT_SENSOR_ENABLED = True

# * This on_message MQTT ISR is used to enable or disable the current sensor (Legacy code, used for expo, disabled on the client side),
# * And to pass MQTT requests to the topic to open / close / stop the door or retrieve the door's current % open 
# * to the door_operation() function to be classified.
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
# * The current sensor doesn't behave as expected... The expected output is a steady logic 1 value to be output when the motor attempts
# * To draw more current than possible. In practice the current sensor spikes to a logic 1 and the returns to logic 0 repeatedly.
# * This variable is used to keep track of the number of spikes detected.
CURRENT_COUNT = 0

# * This is a rising ISR function for GPIO 18 defined in /ControlCode/classes/motor_current.py when current_detect is initialized to the MotorCurrent class.
def current_isr(temp_arg):
    global CURRENT_COUNT
    global CURRENT_SENSOR_ENABLED

    # * CURRENT_SENSOR_ENABLED is a variable created for the expo to disable the current sensor in the event it bugs out. This code has been disabled in the repository.
    if CURRENT_SENSOR_ENABLED:
        
        # * When the number of spikes detected exceed 3, the door is told to stop. Otherwise increment the counter when a spike is detected.
        if CURRENT_COUNT > 4:
            door_operation('stop')
            print("isr called for collision - current")
            mqtt_connect.publish('alerts', 'Object Blocking Door')
            CURRENT_COUNT = 0
        else:
            mqtt_connect.publish('alerts', f"Current Spikes detected: {CURRENT_COUNT}")
            CURRENT_COUNT += 1

current_detect = motor_current.MotorCurrent(isr=current_isr)

# * ------------------------------Operation Loop---------------------------------
# * I think this is to make sure all the threads don't some because the main script reaches the end.. -- Michael
def operation_loop():
    while True:
        pass
        

operation_loop()

