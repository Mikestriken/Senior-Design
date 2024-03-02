import paho.mqtt.client as mqtt
import time

# # MQTT broker details
# broker_address = "10.143.196.35"
# port = 1883
# topic = "rssi"

# # Create MQTT client instance
# client = mqtt.Client()

# """ # Callback function for when the client connects to the broker
# def on_connect(client, userdata, flags, rc):
#     print("Connected to MQTT broker with result code "+str(rc))
#     # Once connected, publish a message
#     client.publish(topic, "Hello MQTT!")
#     print("Message published") """
    
# def on_message(client, userdata, msg):
#     # This function is called everytime the topic is published to.
#     # If you want to check each message, and do something depending on
#     # the content, the code to do this should be run in this function
    
#     print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
    
#     # The message itself is stored in the msg variable
#     # and details about who sent it are stored in userdata

# # Set up connection callback
# # client.on_connect = on_connect
# client.on_message = on_message

# # Connect to broker
# client.connect(broker_address, port)
# client.subscribe(topic)

# # Start the MQTT client loop
# client.loop_forever()

# # Keep the script running for a while to ensure the message is published
# time.sleep(1)

# for i in range(0, 5):
#     print(i)

# # client.loop_stop()

# # Disconnect from the broker
# client.disconnect()

# MQTT broker details
broker_address = "localhost"
mqtt_topic = "weather_topic" # rssi
port = 1883

unacked_publish = set()

# Create MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Callback function for when the publisher connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code ", str(rc))
    
# def on_publish(client, userdata, mid):
#     # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
#     print("data published")
    """ try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !") """

# Set up connection callback
client.on_connect = on_connect
# client.on_publish = on_publish

# Connect to broker
client.connect(broker_address, port)

# Start the background MQTT client loop thread
client.loop_start()

while True:
    client.publish(mqtt_topic, "DAAATAAA!")
    
client.loop_stop()