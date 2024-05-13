##################################################################################
#                         Fan Operation Python Script
# This python script implements the fan control code that turns on / off and sets
# the speed of the fan when requested by other scripts.
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
# Commented by Michael Marais for EPRI_SPOT, Spring 2024
##################################################################################
 
from classes import fan, mqtt_connection
import time

# * Initialize fan GPIO object to control relays
fan = fan.Fan()

# * ------------------------------ Fan MQTT Classifier ---------------------------------
# * MQTT requests are classified by this function below:
def fan_operation(action):
    # * If the message is "fast", set the fan speed to fast and acknowledge that the fan is set to fast
    if action == 'fast':
        fan.power_on()
        mqtt_connect.publish('fan', 'is_fast')
        
    # * If the message is "slow", set the fan speed to slow and acknowledge that the fan is set to slow
    elif action == 'slow':
        fan.speed_low()
        mqtt_connect.publish('fan', 'is_slow')
        
    # * If the message is "stop", turn off the fan and acknowledge that the fan is turned off
    elif action == 'stop':
        fan.power_off()
        mqtt_connect.publish('fan', 'is_off')
        
    # * If the message is 'query_state', respond with the current state of the fan.
    elif action == 'query_state':
        # * if the state is on and fast, respond 'is_fast'
        if fan.is_on and fan.is_fast:
            mqtt_connect.publish('fan', 'is_fast')
            print('published')
            
        # * otherwise, if the state is just on, respond 'is_slow'
        elif fan.is_on:
            mqtt_connect.publish('fan', 'is_slow')
            print('published')
            
        # * otherwise, if the state is off, respond 'is_off'
        else:
            mqtt_connect.publish('fan', 'is_off')
            print('published')
    else:
        print('Invalid action posted to topic: fan ' + str(action))

# * ------------------------------ MQTT ISR ---------------------------------
# * When a message is detected on the 'fan' MQTT topic, the message is passed to the fan_operation() function
# * to be classified and applied.
def on_message_main(self, client, msg):
        # Deserialize JSON data
        # deserialized_data = json.loads(msg.payload)

        print(msg.payload.decode("utf-8"))

        if msg.topic == 'fan':
            fan_operation(msg.payload.decode("utf-8"))

mqtt_connect = mqtt_connection.MQTT_Connection(topics=['fan'], on_message=on_message_main)

# * On startup ensure the fan is set to off.
fan.power_off()

# * I think this code is here to keep this script (which mostly consists of ISRs) running in the background and to cleanup in the event of an error.
try:
    while True:
        pass

finally:
    fan.power_off()