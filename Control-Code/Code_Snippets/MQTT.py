import paho.mqtt.client as mqtt

# * ----------------------------------------- MQTT Publisher -----------------------------------------
# MQTT broker details
broker_address = "localhost"
mqtt_topic = "weather_topic"
port = 1883

# Create MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Callback function for when the publisher connects to the broker
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected!")

# Set up connection callback
client.on_connect = on_connect

# Connect to broker
client.connect(broker_address, port)

# Start the background MQTT client loop thread
client.loop_start()

# * Publish the Data in your main loop
client.publish(mqtt_topic, "data")

# Disconnect MQTT client
client.loop_stop()
client.disconnect()


# * ----------------------------------------------------- MQTT Subscriber -----------------------------------------------------
# MQTT broker details
broker_address = "localhost"
port = 1883
subscriberTopics = ["weather_topic"]

# * Callback function for when a message is received
def on_message(client, userdata, msg):
    # Deserialize JSON data
    deserialized_data = json.loads(msg.payload)
    
    if msg.topic == "weather_topic":
        # * Update Global Variables / Classes here.
        print("Updated weather_data.")

# Create MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set up message callback
client.on_message = on_message

# Connect to broker
client.connect(broker_address, port)

# Subscribe to topic
for i in range(0, len(subscriberTopics)):
    client.subscribe(subscriberTopics[i])

# Start the MQTT client loop
client.loop_forever()