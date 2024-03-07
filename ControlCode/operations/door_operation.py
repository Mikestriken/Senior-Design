import threading
import json

from classes import ultrasonic, door, limit_switch, mqtt_connection

#import RPi.GPIO as GPIO # or gpio setup
#GPIO.setwarnings(False)


# * ------------------------------Door Operation-----------------------------------

front_door = door.Door()
door_limit_switch = limit_switch.LimitSwitch(front_door.door_collision_isr())
door_ultrasonic = ultrasonic.Ultrasonic() # y axis detect

def door_operation(action):
    if action == 'open':
        front_door.open_door()
    elif action == 'close':
        front_door.close_door()
    elif action == 'stop':
        front_door.stop_door()

# * ------------------------------Mqtt Connection-----------------------------------

def on_message_main(msg):
        # Deserialize JSON data
        deserialized_data = json.loads(msg.payload)
        
        if msg.topic == 'door':
            door_operation(msg.payload)
                  
mqtt_connect = mqtt_connection.MQTT_Connection(type='both', topics = ['door'], on_message=on_message_main)

# * ------------------------------Ultrasonic-----------------------------------

def ultrasonic_operation():
    while True:
        if door_ultrasonic.get_average_distance(5) < 100:
            if front_door.get_percent_open < 2:
                door_operation('stop')
                mqtt_connect.publishAsJSON('alert', 'Object Blocking Door')

            if front_door.get_percent_open > 10:
                door_operation('stop')
                mqtt_connect.publishAsJSON('alert', 'Object Blocking Door')

ultrasonic_thread = threading.Thread(target=ultrasonic_operation)
ultrasonic_thread.start()


