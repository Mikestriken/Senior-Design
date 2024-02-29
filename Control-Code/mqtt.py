

def on_message(client, userdata, msg):
    # Deserialize JSON data
    deserialized_data = json.loads(msg.payload)
    
    if msg.topic == "weather_topic":
        data_handler.update_current_data({'weather_data': deserialized_data})
        # currentData['weather_data'] = deserialized_data
        print("Updated weather_data.")