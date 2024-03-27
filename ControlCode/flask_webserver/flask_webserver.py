##############################################################################
#                                 Flask Web Server
#
# Created by Joelle Bailey, Michael Marais for EPRI_SPOT, Spring 2024
#
# to run webserver:  python -B -m flask_webserver.flask_webserver
##############################################################################

from classes.data_handler import DataHandler
from classes.mqtt_connection import MQTT_Connection


# webserver imports
from flask import Flask, request, redirect, url_for, render_template, Response, jsonify
from flask_socketio import SocketIO
import threading
import sys
import socket
import subprocess
import os

# * flag to remove camera code via command-line using --no-camera
cameraCodeFlag = True
if "--no-camera" in sys.argv:
    cameraCodeFlag = False
    
# * flag to enable debugging via command-line using --debug
# Note 1: When debugging is enabled, two instances of this python script will be ran in the console, so you may see double the results.
# Note 2: Enabling debugging makes it so that changes to this python script will automatically reload the server to verify changes
debugFlag = False
if "--debug" in sys.argv:
    debugFlag = True

# camera imports
import time
if cameraCodeFlag:
    import classes.indoor_camera
    import classes.outdoor_camera

app = Flask(__name__, template_folder='static')
socketio = SocketIO(app, cors_allowed_origins='*')

# * ----------------------------------------------------- MQTT and state storage -----------------------------------------------------
# Todo: Merge all the MQTT data handlers into a single datahander and implement custom onmessage that checks the message before deciding what to do.
                                                        # * Alert MQTT
# * Template for how the data should be formatted.
alert_template_data = {
            'alert': None
        }

# * MQTT topics to subscribe to
alert_topic = 'alert'

# * alert_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
alert_data_handler = DataHandler(alert_template_data)
alert_mqtt_connect = MQTT_Connection("subscriber", alert_topic, alert_data_handler, "string")

                                                        # * Wall Power MQTT
# * Template for how the data should be formatted.
wall_power_template_data = {
            'wall_power': None
        }

# * MQTT topics to subscribe to 
wall_power_topic = 'wall_power'

# * wall_power_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
wall_power_data_handler = DataHandler(wall_power_template_data)
wall_power_mqtt_connect = MQTT_Connection("subscriber", wall_power_topic, wall_power_data_handler, "string")

# * Request an update on the current wall power status:
wall_power_mqtt_connect.publish(wall_power_topic + "_request", "update")

                                                        # * Outdoor Weather MQTT
# * Template for how the data should be formatted.
outdoor_weather_template_data = {
            'outdoor_weather': {
                'wind': {
                    'speed': None,
                    'rawDirection': None,
                    'trueDirection:': None,
                    'status': None
                },
                'heading': None,
                'meteorological': {
                    'pressureMercury': None,
                    'pressureBars': None,
                    'temperature': None,
                    'humidity' : None,
                    'dewPoint': None
                }
            }
        }

# * MQTT topics to subscribe to that will update the states.
outdoor_weather_topic = 'outdoor_weather'

# * outdoor_weather_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
outdoor_weather_data_handler = DataHandler(outdoor_weather_template_data)
outdoor_weather_mqtt_connect = MQTT_Connection("subscriber", outdoor_weather_topic, outdoor_weather_data_handler, "json")

                                                        # * Indoor Weather MQTT
# * Template for how the data should be formatted.
indoor_weather_template_data = {
            'indoor_weather': {
                'temperature' : None,
                'relative_humidity' : None
            }
        }

# * MQTT topics to subscribe to that will update the states.
indoor_weather_topic = 'indoor_weather'

# * indoor_weather_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
indoor_weather_data_handler = DataHandler(indoor_weather_template_data)
indoor_weather_mqtt_connect = MQTT_Connection("subscriber", indoor_weather_topic, indoor_weather_data_handler, "json")

                                                        # * Spot Battery
# * Template for how the data should be formatted.
spot_battery_template_data = {
            'battery_state': None
        }

# * MQTT topics to subscribe to 
spot_battery_topic = 'battery_state'

# * spot_battery_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
spot_battery_data_handler = DataHandler(spot_battery_template_data)
spot_battery_mqtt_connect = MQTT_Connection("subscriber", spot_battery_topic, spot_battery_data_handler, "string")

# * Request an update on the current spot battery state:
# spot_battery_mqtt_connect.publish(spot_battery_topic + "_request", "update")

                                                        # * Door
# * Template for how the data should be formatted.
door_template_data = {
            'door': None
        }

# * MQTT topics to subscribe to 
door_topic = 'door'

# * door_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
door_data_handler = DataHandler(door_template_data)
door_mqtt_connect = MQTT_Connection("subscriber", door_topic, door_data_handler, "string")

# * Request an update on the current door state:
door_mqtt_connect.publish(door_topic, "query_state")

                                                        # * Outdoor Light
# * Template for how the data should be formatted.
outdoor_light_template_data = {
            'outdoor_light': None
        }

# * MQTT topics to subscribe to 
outdoor_light_topic = 'outdoor_light'

# * outdoor_light_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
outdoor_light_data_handler = DataHandler(outdoor_light_template_data)

outdoor_light_mqtt_connect = MQTT_Connection("subscriber", outdoor_light_topic, outdoor_light_data_handler, "string")

# * Request an update on the current light state:
outdoor_light_mqtt_connect.publish(outdoor_light_topic, "query_state")

                                                        # * Indoor Light
# * Template for how the data should be formatted.
indoor_light_template_data = {
            'indoor_light': None
        }

# * MQTT topics to subscribe to 
indoor_light_topic = 'indoor_light'

# * indoor_light_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
indoor_light_data_handler = DataHandler(indoor_light_template_data)
indoor_light_mqtt_connect = MQTT_Connection("subscriber", indoor_light_topic, indoor_light_data_handler, "string")

# * Request an update on the current light state:
indoor_light_mqtt_connect.publish(indoor_light_topic, "query_state")

                                                        # * Fan
# * Template for how the data should be formatted.
fan_template_data = {
            'fan': None
        }

# * MQTT topics to subscribe to 
fan_topic = 'fan'

# * fan_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
fan_data_handler = DataHandler(fan_template_data)
fan_mqtt_connect = MQTT_Connection("subscriber", fan_topic, fan_data_handler, "string")

# * Request an update on the current fan state:
fan_mqtt_connect.publish(fan_topic, "query_state")

# * ----------------------------------------------------- Landing Page Functionality -----------------------------------------------------
# * List of datahandler objects to refresh when a new client connects / refreshes
dataHandlerTopics = [indoor_weather_topic, outdoor_weather_topic, wall_power_topic, spot_battery_topic, door_topic, outdoor_light_topic, indoor_light_topic, fan_topic]
dataHandlers = [indoor_weather_data_handler, outdoor_weather_data_handler, wall_power_data_handler, spot_battery_data_handler, door_data_handler, outdoor_light_data_handler, indoor_light_data_handler, fan_data_handler]

# * Run code after a template has been rendered and response is about to be sent.
    # * This code sets the update flag, so that all the SSE generate event generator function instances will send updates to the client
    # * TL;DR This code syncs the client up whenever refreshes / loads the page.
@app.after_request
def after_request(response):
    for DH in dataHandlers:
        print("set DH update flag!")
        DH.set_update_flag()
    
    return response

# * Redirect to index.html if trying to load root page.
@app.route("/")
def root():
    return redirect(url_for('main'))

@app.route("/index.html")
def main():
    return render_template('index.html')

# * ------------------------------------------ Web Sockets ------------------------------------------
def generate_socket_events(socket_topics, data_handler):
    # * Socket_topics should be string or list of strings of topics to send the current state to
    if isinstance(socket_topics, str):
        # Convert single string to a list with a single element
        socket_topics_list = [socket_topics]
    elif isinstance(socket_topics, list):
        # Check all elements of the list are of type string before assigning
        if all(isinstance(s, str) for s in socket_topics):
            socket_topics_list = socket_topics
        else:
            raise TypeError(f"Error: All elements of socket_topic list must be strings. Received: {socket_topics}")
    else:
        raise TypeError("Error: topic must be a string or a list of strings")
    
    
    # * data_handler should be DataHandler or list of DataHandlers
    if isinstance(data_handler, DataHandler):
        # Convert single DataHandler to a list with a single element
        data_handler_list = [data_handler]
    elif isinstance(data_handler, list):
        # Check length of both data_handler and socket_topic match
        if (len(socket_topics) != len(data_handler)):
            raise TypeError(f"Error: Number of elements in data_handler must equal socket_topic:\n{data_handler}\n{socket_topics}")
            
        # Check all elements of the list are of type DataHandler before assigning
        if all(isinstance(DH, DataHandler) for DH in data_handler):
            data_handler_list = data_handler
        else:
            raise TypeError(f"Error: All elements of data_handler list must be type DataHandler. Received: {data_handler}")
    else:
        raise TypeError("Error: topic must be a DataHandler or a list of DataHandlers")
    
    # * Send data to connected clients
    for i in range(len(data_handler_list)):
        if data_handler_list[i].get_update_flag():
            data_handler_list[i].unset_update_flag()
            
            current_data = data_handler_list[i].get_current_data()
            
            # print(f"{socket_topic[i]}: {current_data}")
            socketio.emit(socket_topics_list[i], current_data)
        
socket_thread = None
socket_thread_lock = threading.Lock()

def background_thread():
    while True:
        generate_socket_events([alert_topic] + dataHandlerTopics, [alert_data_handler] + dataHandlers)
        socketio.sleep(1)

@socketio.on('connect')
def connect():
    global socket_thread
    print('Client connected')

    global socket_thread
    with socket_thread_lock:
        if socket_thread is None:
            socket_thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

# * ------------------------------------------ Control Modules ------------------------------------------
                    # Camera
if cameraCodeFlag:
    def gen(camera):
        while True:
            frame = indoor_camera.Camera().get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def gen2(camera):
        while True:
            frame = outdoor_camera.Camera_outdoor().get_frame()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
    @app.route('/indoor_video_feed')
    def indoor_video_feed():
        return Response(gen(indoor_camera.Camera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/outdoor_video_feed')
    def outdoor_video_feed():
        return Response(gen2(outdoor_camera.Camera_outdoor()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        #return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

                    # Door
door_mqtt_connect = MQTT_Connection("publisher")

@app.route("/<object>/<action>")
def action(object, action):
    print("Action Called")
    # MQTT Section
    # * Open Button  → /openButton/click  → openButton_topic,  "click"
    # * Close Button → /closeButton/click → closeButton_topic, "click"
    if object == "openButton" or object == "closeButton":
        door_mqtt_connect.publish(object, action)
        
    # * Fan slider position change to: 0/1/2 => set speed to: stop/slow/fast
    elif object == "fanSlider":
        if action == '0':
            fan_mqtt_connect.publish(fan_topic, "stop")
        elif action == '1':
            fan_mqtt_connect.publish(fan_topic, "slow")
        elif action == '2':
            fan_mqtt_connect.publish(fan_topic, "fast")
        
    # * light slider position change to: 0/1 => set to: on/off
    elif object == "indoorLightSlider":
        if action == '0':
            fan_mqtt_connect.publish(indoor_light_topic, "off")
        elif action == '1':
            fan_mqtt_connect.publish(indoor_light_topic, "on")
        
    # * light slider position change to: 0/1 => set to: on/off
    elif object == "outdoorLightSlider":
        if action == '0':
            fan_mqtt_connect.publish(outdoor_light_topic, "off")
        elif action == '1':
            fan_mqtt_connect.publish(outdoor_light_topic, "on")
    
    # localhost button Section
    # * Reboot Button → /localhost/reboot → Reboot Raspberry Pi
    elif object == "localhost" and action == "reboot":
        subprocess.run(['sudo', 'reboot'])
        
    return redirect(url_for('main'))

# * ----------------------------------------------------- Host Local Website with Debugging Enabled -----------------------------------------------------
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=80, debug=debugFlag)