import multiprocessing
import json
import sys

from classes import ultrasonic, door, limit_switch, mqtt_connection

#import RPi.GPIO as GPIO # or gpio setup
#GPIO.setwarnings(False)

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
        mqtt_connect.publishAsJSON('door', str(front_door.percent_open()))
    else:
        print('Invalid action posted to topic: door' + str(action))

def door_collision_isr():
        door_operation('stop')
        print("collision detected")

door_limit_switch = limit_switch.LimitSwitch(limit_isr=door_collision_isr)

# * ------------------------------Mqtt Connection-----------------------------------

def on_message_main(self, client, msg):
        # Deserialize JSON data
        #deserialized_data = json.loads(msg.payload)
        
        with open('/home/eprispot/Desktop/readme.txt', 'w') as f:
            f.write(msg.payload.decode("utf-8"))

        if msg.topic == 'door':
            door_operation(msg.payload.decode("utf-8"))
                  
mqtt_connect = mqtt_connection.MQTT_Connection(type='both', topics = ['door'], on_message=on_message_main)


def rssi_eval(rssi_value):
    if rssi_value < -80:
        door_operation('open')
    elif rssi_value > -60:
        door_operation('close')


def on_message_rssi(self, client, msg):
        # Deserialize JSON data
        #deserialized_data = json.loads(msg.payload)
        
        with open('/home/eprispot/Desktop/readme.txt', 'w') as f:
            f.write(msg.payload.decode("utf-8"))

        if msg.topic == 'rssi':
            print(msg.payload)
            rssi_eval(int(msg.payload))

rssi_mqtt = mqtt_connection.MQTT_Connection(type='both', topics = ['rssi'], on_message=on_message_rssi, broker_address = "10.143.204.58")

# * ------------------------------Ultrasonic-----------------------------------

def ultrasonic_operation():
    while True:
        reading = door_ultrasonic.get_average_distance(5)
        if reading < 30:
            if front_door.get_percent_open() < 2:
                door_operation('stop')
                mqtt_connect.publishAsJSON('alert', 'Object Blocking Door')
                print('stopped from ultrasonic, reading: ' + str(reading) + 'cm')

            if front_door.get_percent_open() > 10:
                door_operation('stop')
                mqtt_connect.publishAsJSON('alert', 'Object Blocking Door')
                print('stopped from ultrasonic, reading: ' + str(reading) + 'cm')


#ultrasonic_thread = threading.Thread(target=ultrasonic_operation, args = (exit_event,))
#ultrasonic_thread.start()

ultrasonic_operation()

