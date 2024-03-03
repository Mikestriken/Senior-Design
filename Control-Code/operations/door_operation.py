import threading
import json

from ..modules import ultrasonic, door, limit_switch

from ..webserver import mqtt_connection

#import RPi.GPIO as GPIO # or gpio setup
#GPIO.setwarnings(False)


# * ------------------------------Door Operation-----------------------------------

front_door = door.Door()
door_limit_switch = limit_switch.LimitSwitch(front_door.door_collision_isr())
door_ultrasonic = ultrasonic.Ultrasonic() # y axis detect

exit_event = threading.Event()
open_thread = threading.Thread(target=front_door.open_door(), args=(exit_event,))
close_thread = threading.Thread(target=front_door.close_door(), args=(exit_event,))

def door_operation(action):
    if action == 'open':
        open_thread.start()
    elif action == 'close':
        close_thread.start()
    elif action == 'stop':
        front_door.stop_door()
        exit_event.set()        # exits other threads open, close

# * ------------------------------Mqtt Connection-----------------------------------

def on_message_main(msg):
        # Deserialize JSON data
        deserialized_data = json.loads(msg.payload)
        
        if msg.topic == 'door':
            door_operation(msg.payload)
                  
mqtt_connect = mqtt_connection.MQTT_Connection(topics = ['door'])
mqtt_connect.client.on_message = on_message_main

# * ------------------------------Ultrasonic-----------------------------------

def ultrasonic_operation():
    while True:
        if door_ultrasonic.get_average_distance(5) < 100:
            if open_thread.is_alive() and front_door.get_percent_open < 2:
                door_operation('stop')
                mqtt_connect.publish('alert', 'Object Blocking Door')

            if close_thread.is_alive() and front_door.get_percent_open > 10:
                door_operation('stop')
                mqtt_connect.publish('alert', 'Object Blocking Door')

ultrasonic_thread = threading.Thread(target=ultrasonic_operation)
ultrasonic_thread.start()


