import paho.mqtt.client as mqtt
import time

# MQTT broker details
broker_address = "test.mosquitto.org"
port = 1883
topic = "test/topic"

# Callback function for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))
    # Once connected, publish a message
    client.publish(topic, "Hello MQTT!")
    print("Message published")

# Create MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set up connection callback
client.on_connect = on_connect

# Connect to broker
client.connect(broker_address, port)

# Start the MQTT client loop
client.loop_start()

# Keep the script running for a while to ensure the message is published
time.sleep(5)

# Disconnect from the broker
client.disconnect()
