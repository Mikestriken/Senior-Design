import paho.mqtt.client as mqtt

mqtt_topic = "weather_topic"
mqtt_broker_ip = "localhost"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, reason_code, properties):
    print ("Connected")
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):
    print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))

client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, 1883)

client.loop_forever()
client.disconnect()