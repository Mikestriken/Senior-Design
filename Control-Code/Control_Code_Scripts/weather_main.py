import asyncio
import sys

import Classes.weather_class as weather_class

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
weather_station = weather_class.WeatherStation(baud, port)

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
