from classes import fan, mqtt_connection

import time

fan = fan.Fan()
mqtt_connection = mqtt_connection.MQTT_Connection(topics=['fan'])


def fan_operation(action):
    if action == 'fast':
        fan.power_on()
    elif action == 'slow':
        fan.speed_low()
    elif action == 'stop':
        fan.power_off()
    else:
        print('Invalid action posted to topic: fan' + str(action))

def on_message_main(self, client, msg):
        # Deserialize JSON data
        #deserialized_data = json.loads(msg.payload)

        if msg.topic == 'fan':
            fan_operation(msg.payload.decode("utf-8"))


while True:
    time.sleep(1)