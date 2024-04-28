##################################################################################
#                         Weather Station Main Python Script
# This python script instantiates the WeatherStation class defined in
# /ControlCode/classes/weather_class.py which then reads the ASCII output sent by
# the weather station using the NMEA 0183 protocol.
# 
# It then filters the data and sends only the relevant data via MQTT
# 
# Created by Michael Marais for EPRI_SPOT, Spring 2024
##################################################################################

import asyncio
import sys

from classes.weather_class import WeatherStation

# * ----------------------------------------------------- Command Line Debugging Flags -----------------------------------------------------
# * flag to display raw data from weather station via command line using --raw-data
rawDataFlag = False
if "--raw-data" in sys.argv:
    rawDataFlag = True

# * flag to prevent read_and_update_forever from being called via command line using --no-update
noUpdateFlag = False
if "--no-update" in sys.argv:
    noUpdateFlag = True

# * flag to prevent read_and_update_forever from being called via command line using --show-published
displayPublishedDataFlag = False
if "--show-published" in sys.argv:
    displayPublishedDataFlag = True

# * flag to prevent read_and_update_forever from being called via command line using --show-updated
displayUpdatedDataFlag = False
if "--show-updated" in sys.argv:
    displayUpdatedDataFlag = True

# * ----------------------------------------------------- Weather Station Initialization -----------------------------------------------------
port = "ttyUSB0"
baud = 4800
weather_station = WeatherStation(baud, port)

# * ----------------------------------------------------- Weather Station Running -----------------------------------------------------

# * Raw data output if --raw-data command line argument is passed, 
#   Note: MQTT data will not be published
if noUpdateFlag and rawDataFlag:
        while True:
                print(weather_station.get_line())
elif noUpdateFlag:
        sys.exit()

# * Run the weather station asynchronously
asyncio.run(weather_station.read_and_update_forever(rawDataFlag, displayPublishedDataFlag, displayUpdatedDataFlag))
