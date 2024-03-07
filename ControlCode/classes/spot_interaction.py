from ControlCode.webserver import mqtt_connection
import json
import time


def on_message_main(msg):
        # Deserialize JSON data
        deserialized_data = json.loads(msg.payload)
        
        if msg.topic == 'rssi':
            print(msg.payload)

mqtt_connect = mqtt_connection.MQTT_Connection(topics = ['rssi'])
mqtt_connect.client.on_message = on_message_main

while True:
    time.sleep(1)