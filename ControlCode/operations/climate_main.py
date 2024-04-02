import classes.indoor_temp as indoor_temp
from classes.mqtt_connection import MQTT_Connection

indoor_temp_shtc3 = indoor_temp.Indoor_Temp()

HIGH_SPEED_TEMP = 30
LOW_SPEED_TEMP = 20
OFF_TEMP = 10

MANUAL_MODE = False

def on_message_mode(self, client, msg):
        global MANUAL_MODE

        if msg.topic == 'mode':
            if msg.payload.decode("utf-8") == 'manual':
                MANUAL_MODE = True
            elif msg.payload.decode("utf-8") == 'automatic':
                MANUAL_MODE = False

mode_listener = MQTT_Connection(type='subscriber', topics=['mode'], on_message=on_message_mode)

while(1):
    temp, humid = indoor_temp_shtc3.get_reading()

    if MANUAL_MODE == False:
        if temp > HIGH_SPEED_TEMP:
            indoor_temp_shtc3.mqtt_client.publish('fan', 'fast')
        elif temp > LOW_SPEED_TEMP:
            indoor_temp_shtc3.mqtt_client.publish('fan', 'slow')
        elif temp < OFF_TEMP:
            indoor_temp_shtc3.mqtt_client.publish('fan', 'stop')

    indoor_temp_shtc3.publish_reading(temp, humid)