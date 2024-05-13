##################################################################################
#                         Climate Control Main Python Script
# This python script retrieves temperature data from the internal temperature sensor
# (the SHTC3 using I2C), and then uses that to determine if it should turn on
# the fan and if so, at what speed.
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
# Commented by Michael Marais for EPRI_SPOT, Spring 2024
##################################################################################

import classes.indoor_temp as indoor_temp
from classes.mqtt_connection import MQTT_Connection

# * Initialize temperature sensor control code
indoor_temp_shtc3 = indoor_temp.Indoor_Temp()

# * Threshold for fan speed are set below
HIGH_SPEED_TEMP = 30
LOW_SPEED_TEMP = 20
OFF_TEMP = 10

MANUAL_MODE = False

# * The user can set the fan to manual mode and back to automatic mode on the HMI, requests to do so are handled in the on_message function below.
def on_message_mode(self, client, msg):
        global MANUAL_MODE

        # * This script handles the automated fan control. When manual mode is requested, it disables the automated climate control,
        # * but it does not acknowledge the request unfortunately.
        # ! There could be a risk of this script going out of sync with the /ControlCode/operations/fan_operation.py script in an edge case due to there being no acknowledgement.
        if msg.topic == 'fan_HOA':
            if msg.payload.decode("utf-8") == 'manual':
                MANUAL_MODE = True
            elif msg.payload.decode("utf-8") == 'automatic':
                MANUAL_MODE = False

mode_listener = MQTT_Connection(type='subscriber', topics=['fan_HOA'], on_message=on_message_mode)

# * Main operation loop of this script
while(1):
    # * 1. Retrieve temperature and humidity readings.
    temp, humid = indoor_temp_shtc3.get_reading()

    # * 2. If not in manual mode:
    if MANUAL_MODE == False:
        # * 2.a) If temperature exceeds HIGH_SPEED_TEMP, set the fan speed to fast
        if temp > HIGH_SPEED_TEMP:
            indoor_temp_shtc3.mqtt_client.publish('fan', 'fast')
            
        # * 2.b) If temperature exceeds LOW_SPEED_TEMP, set the fan speed to slow
        elif temp > LOW_SPEED_TEMP:
            indoor_temp_shtc3.mqtt_client.publish('fan', 'slow')
            
        # * 2.c) If temperature is less than OFF_TEMP, turn the fan off.
        elif temp < OFF_TEMP:
            indoor_temp_shtc3.mqtt_client.publish('fan', 'stop')

    # * 3. Send indoor temperature sensor readings to the 'indoor_weather' MQTT Topic for the webserver to display on the HMI.
    indoor_temp_shtc3.publish_reading()