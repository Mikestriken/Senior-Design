import paho.mqtt.client as mqtt
import json

class MQTT_Connection():
    def __init__(self, on_message,  data_handler, topics = [], broker_address = "localhost", port = 1883):
        self.data_handler = data_handler
        self.topics = topics

        # Create MQTT client instance
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        # Set up message callback
        if on_message == None:
            self.client.on_message = self.on_message
        else:
            self.client.on_message = on_message

        # Connect to broker
        self.client.connect(broker_address, port)

        # Subscribe to topics
        for topic in topics:
            self.client.subscribe(topic)

        # Start the MQTT client loop
        self.client.loop_forever()

    # * Callback function for when a message is received
    def on_message(self, msg):
        # Deserialize JSON data
        deserialized_data = json.loads(msg.payload)
        
        for topic in self.topics:
            if topic == msg.topic and self.data_handler is not None:
                self.data_handler.update_current_data({topic: deserialized_data})
                print("Updated " + topic)
    
    def publish(self, topic, currentData):
        jsonData = json.dumps(currentData)
        self.client.publish(topic, jsonData)

    def __del__(self):
        # Disconnect MQTT client
        self.client.loop_stop()
        self.client.disconnect()
        

