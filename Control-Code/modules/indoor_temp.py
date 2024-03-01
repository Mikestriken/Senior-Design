##############################################################################
#                                 Indoor Temperature
# Indoor temperature sensor module for SHTC3
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##############################################################################

import time
import board
import adafruit_shtc3

class Indoor_Temp():
    def __init__(self):
        self.i2c = board.I2C()   # uses board.SCL and board.SDA
        self.sht = adafruit_shtc3.SHTC3(self.i2c)
    
    def get_reading(self):
        temperature, relative_humidity = self.sht.measurements
        return temperature, relative_humidity
