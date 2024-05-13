##################################################################################
#                       lighting Operation Python Script
# This python script implements the control code to turn on and off the internal
# lights of the dock house based on MQTT requests from other scripts.
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
# Commented by Michael Marais for EPRI_SPOT, Spring 2024
##################################################################################
 
from classes import lighting, mqtt_connection

import time
import json


import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# * Instantiate the GPIO objects to control the lighting relays. Lights are turn on during initialization.
indoor_light = lighting.Indoor_Lighting()
outdoor_light = lighting.Outdoor_Lighting() # ! This is outdated code. To my knowledge, Outdoor light is not controlled by the Raspberry Pi

# * MQTT ISR, that will classify messages on the 'indoor_light' and 'outdoor_light' MQTT topics into commands to control the relays via GPIO.
def on_message(self, client, msg):
    
    # * Decode the message from byte format
    msg.payload = msg.payload.decode("utf-8")

    # * Filter to relevant topic
    if msg.topic == 'indoor_light':
        # * 'power_on' message => close the relay, acknowledge with 'is_on'
        if msg.payload == 'power_on':
            indoor_light.power_on()
            mqtt_connect.publish('indoor_light', "is_on")
            
        # * 'power_off' message => Open the relay, acknowledge with 'is_off'
        elif msg.payload == 'power_off':
            indoor_light.power_off()
            mqtt_connect.publish('indoor_light', "is_off")
            
        # * 'toggle' message => Open the relay if closed, vice versa
        # Note: Not acknowledged
        elif msg.payload == 'toggle':
            indoor_light.toggle()
            
        # * 'query_state' message => Return current state of the relay (closed / open) => Light on / off
        elif msg.payload == 'query_state':
            if outdoor_light.is_on:
                mqtt_connect.publish('indoor_light', "is_on")
            else:
                mqtt_connect.publish('indoor_light', "is_off")
        else:
            print('Invalid action posted to topic: indoor_light ' + str(msg))

    # ! Obsolete Code below, has same functionality as above but applied to an unused GPIO port
    if msg.topic == 'outdoor_light':
        if msg.payload == 'power_on':
            outdoor_light.power_on()
        elif msg.payload == 'power_off':
            outdoor_light.power_off()
        elif msg.payload == 'toggle':
            outdoor_light.toggle()
        elif msg.payload == 'query_state':
            if outdoor_light.is_on:
                mqtt_connect.publish('outdoor_light', "is_on")
            else:
                mqtt_connect.publish('outdoor_light', "is_off")
        else:
            print('Invalid action posted to topic: outdoor_light ' + str(msg))

mqtt_connect = mqtt_connection.MQTT_Connection(type='both', topics = ['indoor_light', 'outdoor_light'], on_message=on_message)

#-----------------------------------Photoresister Outdoor Light Triggering -----------------------------------------
# ! Obsolete code below. I have no idea what this was supposed to be used for, but I can confirm it is no longer being used.
def photoresister_isr_on():
    outdoor_light.power_on()

def photoresister_isr_off():
    outdoor_light.power_off()

pin_number = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_number, GPIO.IN)

# GPIO.add_event_detect(pin_number, GPIO.RISING, pull_up_down=GPIO.PUD_DOWN,
#     callback=photoresister_isr_on, bouncetime=300)

# GPIO.add_event_detect(pin_number, GPIO.FALLING, pull_up_down=GPIO.PUD_DOWN,
#     callback=photoresister_isr_off, bouncetime=300)

# * I think this code is here to keep this script (which mostly consists of ISRs) running in the background and to cleanup in the event of an error.
try:
    while True:
        pass

finally:
    outdoor_light.power_off()
    mqtt_connect.publishAsJSON('outdoor_light', "is_off")