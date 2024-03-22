from classes import fan, mqtt_connection

import time

fan = fan.Fan()

def fan_operation(action):
    if action == 'fast':
        fan.power_on()
    elif action == 'slow':
        fan.speed_low()
    elif action == 'stop':
        fan.power_off()
    elif action == 'query_state':
        if fan.is_on:
            mqtt_connect.publishAsJSON('fan', 'is_on')
            print('published')
        else:
            mqtt_connect.publishAsJSON('fan', 'is_off')
            print('published')
    else:
        print('Invalid action posted to topic: fan ' + str(action))

def on_message_main(self, client, msg):
        # Deserialize JSON data
        # deserialized_data = json.loads(msg.payload)

        print(msg.payload.decode("utf-8"))

        if msg.topic == 'fan':
            fan_operation(msg.payload.decode("utf-8"))
            
mqtt_connect = mqtt_connection.MQTT_Connection(topics=['fan'], on_message=on_message_main)

try:
    while True:
        time.sleep(1)

finally:
    fan.power_off()