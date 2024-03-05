import Classes.data_handler as data_handler
import Classes.mqtt_connection as mqtt_connection

template_data = {
            'weather_data': {
                'wind': {
                    'speed': "...",
                    'direction': "...",
                    'status': "..."
                },
                'heading': "...",
                'meteorological': {
                    'pressureMercury': "...",
                    'pressureBars': "...",
                    'temperature': "...",
                    'humidity' : "...",
                    'dewPoint': "..."
                }
            },
            'indoor_weather': {
                'temperature' : "...",
                'relative_humidity' : "..."
            }
        }

webserver_topics = ['weather_data', 'indoor_weather']

# * Instantiate a Data_Handler Object with the template_data
    # * this ensures only a single thread is able to update the data at a time.
    # * The two threads that need to access the data stored is the Flask Webserver and MQTT Updater
data_handler = data_handler.DataHandler(template_data)
mqtt_connect = mqtt_connection.MQTT_Connection("subscriber", webserver_topics, data_handler)

while True:
    pass