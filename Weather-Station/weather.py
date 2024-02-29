import serial
import re
import copy

# * Specify the serial port and its baud rate.
ser = serial.Serial('/dev/ttyUSB0', 4800)

# * Dictionary to store the parsed data
currentData = {
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
previousData = copy.deepcopy(currentData)

# * Regex patterns for parsing relevant NMEA sentences
              # Sample Data: $WIMWV,   181.1  ,R,    0.3   ,N,  A    *    29
wind_pattern = re.compile(r'\$WIMWV,(-?[\d.]+),R,(-?[\d.]+),N,([AV])\*(?:\w{2})')

                 # Sample Data: $HCHDT,   81.1   ,T *   11
heading_pattern = re.compile(r'\$HCHDT,(-?[\d.]+),T\*(?:\w{2})')

                        # Sample Data: $WIMDA,  29.2554 ,I,  0.9907  ,B,  23.9    ,C,,,   14.4   ,,  -4.8    ,C,,,,,,,, *   61
meteorological_pattern = re.compile(r'\$WIMDA,(-?[\d.]+),I,(-?[\d.]+),B,(-?[\d.]+),C,,,(-?[\d.]+),,(-?[\d.]+),C,,,,,,,,\*(?:\w{2})')

# * function to check that 'obj' doesn't have any properties or nested objects with value 'None'.
def check_none(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if v is None:
                return True
            if isinstance(v, dict):
                if check_none(v):
                    return True
    return False

# * Main Loop:
try:
    while True:
        # * Read a line of data from the serial port
        line = ser.readline().decode().strip()
        
        # * DEBUG: Check if the received data starts with "" argument
        """ if line.startswith("$HCHDT"):
            print(line) """

        # * Parse the line using regex patterns
        wind_match = wind_pattern.match(line)
        heading_match = heading_pattern.match(line)
        meteorological_match = meteorological_pattern.match(line)
        
        
        # * DEBUG: Print regular expression return
        """ if wind_match:
            print("Wind: " + line)
            print("Direction: " + wind_match.group(1))
            print("Speed: " + wind_match.group(2))
            print("Status: " + wind_match.group(3))
            
        elif heading_match:
            print("Heading: " + line)
            print("Value: " + heading_match.group(1))
            
        elif meteorological_match:
            print("Meteorological: " + line)
            print("Pressure Mercury: " + meteorological_match.group(1))
            print("Pressure Bars: " + meteorological_match.group(2))
            print("Temperature: " + meteorological_match.group(3))
            print("Humidity: " + meteorological_match.group(4) + '%')
            print("Dew Point: " + meteorological_match.group(5)) """
            
        # * Update currentData Properties 
        if wind_match:
            currentData['wind']['direction'] = float(wind_match.group(1))
            currentData['wind']['speed'] = float(wind_match.group(2))
            currentData['wind']['status'] = str(wind_match.group(3))
            
        elif heading_match:
            currentData['heading'] = float(heading_match.group(1))
            
        elif meteorological_match:
            currentData['meteorological']['pressureMercury'] = float(meteorological_match.group(1))
            currentData['meteorological']['pressureBars'] = float(meteorological_match.group(2))
            currentData['meteorological']['temperature'] = float(meteorological_match.group(3))
            currentData['meteorological']['humidity'] = float(meteorological_match.group(4))
            currentData['meteorological']['dewPoint'] = float(meteorological_match.group(5))

        # * 1. Check if previousData is not equal to currentData
        # * 2. Check that currentData doesn't have any properties with the value "None"
        # * 3. Print / Send data
        if previousData != currentData and not check_none(currentData):
            print(currentData)

        # * Update previousData for the next iteration
        previousData = copy.deepcopy(currentData)

# * If Ctrl + C signal sent, close the serial port properly before exiting.
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting...")

finally:
    print("PORT CLOSED!")
    ser.close()
