from classes import lighting, mqtt_connection

import schedule
import time
from datetime import datetime, timezone
import ephem
import json
import pytz

import RPi.GPIO as GPIO

GPIO.setwarnings(False)

indoor_light = lighting.Indoor_Lighting()
outdoor_light = lighting.Outdoor_Lighting()

def on_message(self, client, msg):
    # Deserialize JSON data
    deserialized_data = json.loads(msg.payload)
    
    if msg.topic == 'indoor_light':
        if msg.payload == 'power_on':
            indoor_light.power_on()
        elif msg.payload == 'power_off':
            indoor_light.power_off()
        elif msg.payload == 'toggle':
            indoor_light.toggle()
        elif msg.payload == 'query_state':
            if outdoor_light.is_on:
                mqtt_connect.publishAsJSON('indoor_light', "is_on")
            else:
                mqtt_connect.publishAsJSON('indoor_light', "is_off")
        else:
            print('Invalid action posted to topic: indoor_light ' + str(msg))

    if msg.topic == 'outdoor_light':
        if msg.payload == 'power_on':
            outdoor_light.power_on()
        elif msg.payload == 'power_off':
            outdoor_light.power_off()
        elif msg.payload == 'toggle':
            outdoor_light.toggle()
        elif msg.payload == 'query_state':
            if outdoor_light.is_on:
                mqtt_connect.publishAsJSON('outdoor_light', "is_on")
            else:
                mqtt_connect.publishAsJSON('outdoor_light', "is_off")
        else:
            print('Invalid action posted to topic: outdoor_light ' + str(action))

mqtt_connect = mqtt_connection.MQTT_Connection(topics = ['indoor_light', 'outdoor_light'], on_message=on_message)

#-----------------------------------Photoresister Outdoor Light Triggering -----------------------------------------

def photoresister_isr_on():
    outdoor_light.power_on()

def photoresister_isr_off():
    outdoor_light.power_off()

pin_number = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_number, GPIO.IN)

GPIO.add_event_detect(pin_number, GPIO.RISING, pull_up_down=GPIO.PUD_DOWN,
    callback=photoresister_isr_on, bouncetime=300)

GPIO.add_event_detect(pin_number, GPIO.FALLING, pull_up_down=GPIO.PUD_DOWN,
    callback=photoresister_isr_off, bouncetime=300)


try:
    while True:
        time.sleep(1)

finally:
    outdoor_light.power_off()
    mqtt_connect.publishAsJSON('outdoor_light', "is_off")