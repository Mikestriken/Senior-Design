from classes import lighting, mqtt_connection

import schedule
import time
import ephem
import json

indoor_light = lighting.Indoor_Lighting()
outdoor_light = lighting.Outdoor_Lighting()

def on_message(msg):
    # Deserialize JSON data
    deserialized_data = json.loads(msg.payload)
    
    if msg.topic == 'indoor_light':
        if msg.payload == 'power_on':
            indoor_light.power_on()
        elif msg.payload == 'power_off':
            indoor_light.power_off()
        elif msg.payload == 'toggle':
            indoor_light.toggle()
    if msg.topic == 'outdoor_light':
        if msg.payload == 'power_on':
            outdoor_light.power_on()
        elif msg.payload == 'power_off':
            outdoor_light.power_off()
        elif msg.payload == 'toggle':
            outdoor_light.toggle()

mqtt_connect = mqtt_connection.MQTT_Connection(type = 'subscriber', topics = ['indoor_light', 'outdoor_light'], on_message=on_message)


def calculate_sunrise():
    # Set the observer's location (latitude, longitude)
    observer = ephem.Observer()
    observer.lat = '42.368195'  
    observer.lon = '-73.285858' 

    # Calculate sunrise time
    sunrise_time = observer.next_rising(ephem.Sun())
    return ephem.localtime(sunrise_time)

def calculate_sunset():
    # Set the observer's location (latitude, longitude)
    observer = ephem.Observer()
    observer.lat = '42.368195'  
    observer.lon = '-73.285858' 

    # Calculate sunrise time
    sunset_time = observer.next_setting(ephem.Sun())
    return ephem.localtime(sunset_time)


# Schedule the task at the sunrise time
#schedule.every().day.at(calculate_sunrise.strftime("%H:%M")).do(outdoor_light.power_on)
#schedule.every().day.at(calculate_sunset.strftime("%H:%M")).do(outdoor_light.power_on)

while True:
    indoor_light.power_on()
    time.sleep(0.005)
    indoor_light.power_off()
    time.sleep(0.01)