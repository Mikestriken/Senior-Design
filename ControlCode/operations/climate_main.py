##################################################################################
#                         Climate Control Main Python Script
# This python script retrieves temperature data from the internal temperature sensor
# (the SHTC3 using I2C), and then uses that to determine if it should turn on
# the fan and if so, at what speed.
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##################################################################################

import classes.indoor_temp as indoor_temp
from classes.mqtt_connection import MQTT_Connection

indoor_temp_shtc3 = indoor_temp.Indoor_Temp()

HIGH_SPEED_TEMP = 30
LOW_SPEED_TEMP = 20
OFF_TEMP = 10

MANUAL_MODE = False

def on_message_mode(self, client, msg):
        global MANUAL_MODE

        if msg.topic == 'fan_HOA':
            if msg.payload.decode("utf-8") == 'manual':
                MANUAL_MODE = True
            elif msg.payload.decode("utf-8") == 'automatic':
                MANUAL_MODE = False

mode_listener = MQTT_Connection(type='subscriber', topics=['fan_HOA'], on_message=on_message_mode)

while(1):
    temp, humid = indoor_temp_shtc3.get_reading()

    if MANUAL_MODE == False:
        if temp > HIGH_SPEED_TEMP:
            indoor_temp_shtc3.mqtt_client.publish('fan', 'fast')
        elif temp > LOW_SPEED_TEMP:
            indoor_temp_shtc3.mqtt_client.publish('fan', 'slow')
        elif temp < OFF_TEMP:
            indoor_temp_shtc3.mqtt_client.publish('fan', 'stop')

    indoor_temp_shtc3.publish_reading()