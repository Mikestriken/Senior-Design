##############################################################################
#                                 Indoor Temperature
# Indoor temperature sensor module for SHTC3
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##############################################################################

import time
import board
import adafruit_shtc3
import json
from ..webserver import mqtt_connection

class Indoor_Temp():
    def __init__(self, mqtt_connect = mqtt_connection.MQTT_Connection()):
        self.i2c = board.I2C()   # uses board.SCL and board.SDA
        self.sht = adafruit_shtc3.SHTC3(self.i2c)
        self.mqtt_client = mqtt_connect
    
    def get_reading(self):
        temperature, relative_humidity = self.sht.measurements
        return temperature, relative_humidity
    
    def publish_reading(self):
        temp, humid = self.get_reading()
        data = {'temperature': temp, 'relative_humidity': humid}

        jsonData = json.dumps(self.data)
        self.mqtt_client.publish('indoor_weather', jsonData)
