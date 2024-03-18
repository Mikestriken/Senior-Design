import paho.mqtt.client as mqtt
import json

class MQTT_Connection():
    def __init__(self, type = 'both', topics = None, data_handler = None, on_message_type = None, on_message = None, broker_address = "localhost", port = 1883):
        
        # * Initialize MQTT differently based on type, valid types are "publisher", "subscriber" and "both"
        if type.lower() == "publisher":
            # Create MQTT client instance
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

            # Connect to broker
            self.client.connect(broker_address, port)

            # Start the MQTT client loop
            self.client.loop_start()
            
        elif (type.lower() == "subscriber") or (type.lower() == "both"):
            # * Topics should be string or list of strings for the MQTT client to subscribe to
            if isinstance(topics, str):
                # Convert single string to a list with a single element
                self.topics = [topics]
            elif isinstance(topics, list):
                # Check all elements of the list are of type string before assigning
                if all(isinstance(s, str) for s in topics):
                    self.topics = topics
                else:
                    raise TypeError(f"All elements of topic list must be strings. Received: {topics}")
            else:
                raise TypeError("topic must be a string or a list of strings")
            
            # Create MQTT client instance
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

            # * Ensure an on_message callback is assigned
            if on_message == None:
                # * if on_messaged is defined internally,
                # * a data_handler must be passed by reference,
                # * and be a class with an `.update_current_data` method
                if (isinstance(data_handler, (int, float, str, tuple, list, dict))) and not hasattr(data_handler, 'update_current_data'):
                    raise ValueError(f"subscribers require a data_handler class instance if on_message callback isn't provided: {data_handler != None}, {not isinstance(data_handler, (int, float, str, tuple, list, dict))}\n That has an update_current_data method: {hasattr(data_handler, 'update_current_data')}")
                
                if (on_message_type.lower() != "json") and (on_message_type.lower() != "string"):
                    raise ValueError(f"subscribers require a on_message_type of 'json' or 'string' if on_message callback isn't provided!\non_message_type provided: '{on_message_type}'")
                    
                self.data_handler = data_handler
                self.client.on_message = self.on_message
                self.on_message_type = on_message_type.lower()
                
            else:
                self.client.on_message = on_message

            # Connect to broker
            self.client.connect(broker_address, port)

            # Subscribe to topics
            for topic in self.topics:
                self.client.subscribe(topic)

            # Start the MQTT client loop
            self.client.loop_start()
            
            print(f"Created MQTT Client subscribed to: {self.topics}")
            
        else:
            raise ValueError(f"Invalid MQTT type declaration: {type} must be publisher or subscriber!")

    # * Default, internal callback function for when a message is received
    def on_message(self, client, userdata, msg):
        # * Find out which topic got a message and update the data_hander with the data.
        print(f"New message: {msg.payload} → {msg.payload.decode('utf-8')}")
        try:
            for topic in self.topics:
                if topic == msg.topic:
                    deserialized_data = None
                    
                    if (self.on_message_type == "json"):
                        # Convert payload from JSON into a python equivalent
                        deserialized_data = json.loads(msg.payload)
                        
                    elif (self.on_message_type == "string"):
                        # Directly attach payload to deserialized data
                        deserialized_data = str(msg.payload.decode('utf-8'))
                        
                    else:
                        raise ValueError(f"Invalid Message type declaration during initialization! Type: '{self.on_message_type}' must be 'json' or 'string'!")
                        
                        
                    
                    # Update the data_handler
                    self.data_handler.update_current_data({topic: deserialized_data})
                    # print(f"Updated {topic} with: {deserialized_data}")
                    
                    break # There can only be topic in a message, break out of for loop.
        except Exception as e:
            print(f"Something went Wrong...\nMessage: {msg.payload}\n\nError Log:")
            print(e)
    
    # * Publish data wrapped in JSON method
    def publishAsJSON(self, topic, data):
        # Convert data to JSON Format
        jsonData = json.dumps(data)
        
        # Publish the data
        self.client.publish(topic, jsonData)
    
    # * Publish data method
    def publish(self, topic, data):
        # Publish the data
        self.client.publish(topic, data)

    # * MQTT_Connection Destructor
    def __del__(self):
        # Disconnect MQTT client
        self.client.loop_stop()
        self.client.disconnect()