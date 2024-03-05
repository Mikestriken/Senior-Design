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
import asyncio
import threading
# Even though mqtt_connection is in the same directory (Classes) as weather.py,
# weather.py gets called from a different directory and so the system path is not located in the Classes subdirectory
import Classes.mqtt_connection as mqtt_connection

class WeatherStation():
    def __init__(self, baud=4800, port="ttyUSB0", mqtt_client = mqtt_connection.MQTT_Connection("publisher")):
        # * Specify the serial port and its baud rate.
        try:
            self.ser = serial.Serial('/dev/' + port, baud)
        except Exception as e:
            raise ValueError(f"Serial port couldn't be instantiated with \'/dev/{port}\' at {baud} baud")
        
        # * Threading Lock for Asynchronous Data Updating and Publishing
        self.lock = threading.Lock()
        
        # * UNICODE Decode Error Flag, used in get_line method
        self.UNICODE_ERROR = False
        
        # * When data is updated and different in read_and_update_forever(), this flag will be set and cleared after the new data is published in publish_data()
        self.NEW_DATA_FLAG = False
        
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

        # Initialize previousData with None values
        self.previousData = copy.deepcopy(self.currentData)

        # Add MQTT client to properties of this instance.
        self.client = mqtt_client

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
    
    # * Conventional function that can be used to retrieve the data from the serial port
    def get_line(self):
        # * On startup ASCII art is displayed with the AIRMAR Logo that cannot be decoded with UTF-8,
        # * this will handle that exception but not decoding it if it cannot.
        
        # Clear UNICODE_ERROR Flag because we are about to try again.
        self.UNICODE_ERROR = False
        
        try:
            # Read a line of data from the serial port and decode it
            line = self.ser.readline().decode().strip()
        except UnicodeDecodeError:
            # Handle the exception by skipping decoding and directly returning the bytes
            self.UNICODE_ERROR = True
            line = self.ser.readline().strip()
        
        return line
    
    # * Debugging function that will asynchronously print the raw data while the weather station call operates normally.
    # * Can be enabled if the rawDataFlag is set to true as an argument for the read_and_update_forever function. 
    async def get_line_forever(self):
        # * On startup ASCII art is displayed with the AIRMAR Logo that cannot be decoded with UTF-8,
        # * this will handle that exception but not decoding it if it cannot.
        while True:
            try:
                # Read a line of data from the serial port and decode it
                line = self.ser.readline().decode().strip()
            except UnicodeDecodeError:
                line = self.ser.readline().strip()
            
            print(line)
            
            await asyncio.sleep(0)
    
    async def publish_data(self, displayPublishedDataFlag = False):
        while True:
            # * 1. Check if previousData is not equal to currentData
            # * 2. Check that currentData doesn't have any properties with the value "None"
            # * 3. Print / Send data
            with self.lock:
                if self.NEW_DATA_FLAG:
                    
                    # * Debugging Flag to show the published data
                    if displayPublishedDataFlag:
                        print(f"Published:\n{self.currentData}\n")
                    
                    # Publish
                    self.client.publishAsJSON('weather_topic', self.currentData)
                    
                    # Clear new data flag
                    self.NEW_DATA_FLAG = False
                
            await asyncio.sleep(2) # Wait 2 seconds before publishing again. (to save on bandwidth, just in case)
            
    
    async def read_and_update_forever(self, rawDataFlag = False, displayPublishedDataFlag = False, displayUpdatedDataFlag = False):
        
        asyncio.create_task(self.publish_data(displayPublishedDataFlag))
        
        if rawDataFlag:
            asyncio.create_task(self.get_line_forever())
            
        
        while True:
            # * Attempt to decode a line from the serial port
            line = self.get_line()
            
            # * If failed to decode, break out early.
            if self.UNICODE_ERROR:
                return -1

            # * Parse the line using regex patterns
            wind_match = self.wind_pattern.match(line)
            heading_match = self.heading_pattern.match(line)
            meteorological_match = self.meteorological_pattern.match(line)

            with self.lock:
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
                
                # * Debugging Flag to show the latest internal data
                if displayUpdatedDataFlag:
                    print(f"Updated Data with:\n{self.currentData}\n")
                    
                # * Set new data flag so that publish_data knows it has something new to report
                if (self.previousData != self.currentData) and (not self.check_none(self.currentData)):
                    self.NEW_DATA_FLAG = True
                    
                # * Update previousData for the next iteration
                self.previousData = copy.deepcopy(self.currentData)
                
            await asyncio.sleep(0) # Wait a small amount of time to allow other tasks to be scheduled

    def __del__(self):
        print("PORT CLOSED!")
        self.ser.close()
