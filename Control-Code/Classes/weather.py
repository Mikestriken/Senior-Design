#############################################################################################################
#                                 NMEA Weather Station
#
# Created by Michael Marais refactored by Joelle Bailey for EPRI_SPOT, Spring 2024
#
# * Regex patterns for parsing relevant NMEA sentences
# Sample Data:   $WIMWV,   181.1  ,R,    0.3   ,N,  A    *    29
#              '\$WIMWV,(-?[\d.]+),R,(-?[\d.]+),N,([AV])\*(?:\w{2})'
#
# Sample Data:   $HCHDT,   81.1   ,T *   11
#              '\$HCHDT,(-?[\d.]+),T\*(?:\w{2})'
#
# Sample Data:   $WIMDA,  29.2554 ,I,  0.9907  ,B,  23.9    ,C,,,   14.4   ,,  -4.8    ,C,,,,,,,, *   61
#              '\$WIMDA,(-?[\d.]+),I,(-?[\d.]+),B,(-?[\d.]+),C,,,(-?[\d.]+),,(-?[\d.]+),C,,,,,,,,\*(?:\w{2})'
#############################################################################################################

import serial
import re
import copy
import json
# Even though mqtt_connection is in the same directory (Classes) as weather.py,
# weather.py gets called from a different directory and so the system path is not located in the Classes subdirectory
import Classes.mqtt_connection as mqtt_connection

class WeatherStation():
    def __init__(self, mqtt_client = mqtt_connection.MQTT_Connection("publisher")):
        # * Specify the serial port and its baud rate.
        self.ser = serial.Serial('/dev/ttyUSB0', 4800)

        # * Dictionary to store the parsed data
        self.currentData = {
            'wind': {
                'speed': None,
                'direction': None,
                'status': None
            },
            'heading': None,
            'meteorological': {
                'pressureMercury': None,
                'pressureBars': None,
                'temperature': None,
                'humidity' : None,
                'dewPoint': None
            }
        }

        self.client = mqtt_client

        # Initialize previousData with None values
        self.previousData = copy.deepcopy(self.currentData)

        # * Regex patterns for parsing relevant NMEA sentences
        self.wind_pattern = re.compile(r'\$WIMWV,(-?[\d.]+),R,(-?[\d.]+),N,([AV])\*(?:\w{2})')           
        self.heading_pattern = re.compile(r'\$HCHDT,(-?[\d.]+),T\*(?:\w{2})')                       
        self.meteorological_pattern = re.compile(r'\$WIMDA,(-?[\d.]+),I,(-?[\d.]+),B,(-?[\d.]+),C,,,(-?[\d.]+),,(-?[\d.]+),C,,,,,,,,\*(?:\w{2})')

    # * function to check that an 'object' doesn't have any properties or nested objects with value 'None'.
    def check_none(self, obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if v is None:
                    return True
                if isinstance(v, dict):
                    if self.check_none(v):
                        return True
        return False
    
    def get_line(self):
        # * Read a line of data from the serial port
        line = self.ser.readline().decode().strip()
        return line
    
    def read_and_update(self):
        
        line = self.get_line()

        # * Parse the line using regex patterns
        wind_match = self.wind_pattern.match(line)
        heading_match = self.heading_pattern.match(line)
        meteorological_match = self.meteorological_pattern.match(line)

        # * Update currentData Properties 
        if wind_match:
            self.currentData['wind']['direction'] = float(wind_match.group(1))
            self.currentData['wind']['speed'] = float(wind_match.group(2))
            self.currentData['wind']['status'] = str(wind_match.group(3))
            
        elif heading_match:
            self.currentData['heading'] = float(heading_match.group(1))
            
        elif meteorological_match:
            self.currentData['meteorological']['pressureMercury'] = float(meteorological_match.group(1))
            self.currentData['meteorological']['pressureBars'] = float(meteorological_match.group(2))
            self.currentData['meteorological']['temperature'] = float(meteorological_match.group(3))
            self.currentData['meteorological']['humidity'] = float(meteorological_match.group(4))
            self.currentData['meteorological']['dewPoint'] = float(meteorological_match.group(5))

        # * 1. Check if previousData is not equal to currentData
        # * 2. Check that currentData doesn't have any properties with the value "None"
        # * 3. Print / Send data
        if self.previousData != self.currentData and not self.check_none(self.currentData):
            jsonData = json.dumps(self.currentData)
            self.client.publish('weather_topic', jsonData)

        # * Update previousData for the next iteration
        self.previousData = copy.deepcopy(self.currentData)

    def __del__(self):
        print("PORT CLOSED!")
        self.ser.close()
