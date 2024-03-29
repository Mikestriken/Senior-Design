from classes import fan, mqtt_connection

import time

fan = fan.Fan()

def fan_operation(action):
    if action == 'fast':
        fan.power_on()
        mqtt_connect.publish('fan', 'is_fast')
    elif action == 'slow':
        fan.speed_low()
        mqtt_connect.publish('fan', 'is_slow')
    elif action == 'stop':
        fan.power_off()
        mqtt_connect.publish('fan', 'is_off')
    elif action == 'query_state':
        if fan.is_on and fan.is_fast:
            mqtt_connect.publish('fan', 'is_fast')
            print('published')
        elif fan.is_on:
            mqtt_connect.publish('fan', 'is_slow')
            print('published')
        else:
            mqtt_connect.publish('fan', 'is_off')
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

fan.power_off()

try:
    while True:
        time.sleep(1)

finally:
    fan.power_off()