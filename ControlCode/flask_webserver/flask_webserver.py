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
    import indoor_camera, outdoor_camera

app = Flask(__name__, template_folder='static')
socketio = SocketIO(app, cors_allowed_origins='*')

# * ----------------------------------------------------- MQTT and state storage -----------------------------------------------------
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

# * alert_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
wall_power_data_handler = DataHandler(wall_power_template_data)
wall_power_mqtt_connect = MQTT_Connection("subscriber", wall_power_topic, wall_power_data_handler, "string")

# * Request an update on the current wall power status:
wall_power_mqtt_connect.publish(wall_power_topic + "_request", "update")

                                                        # * Weather MQTT
# * Template for how the data should be formatted.
weather_template_data = {
            'weather': {
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
            },
            'indoor_weather': {
                'temperature' : None,
                'relative_humidity' : None
            }
        }

# * MQTT topics to subscribe to that will update the states.
weather_topics = ['weather', 'indoor_weather']

# * weather_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
weather_data_handler = DataHandler(weather_template_data)
weather_mqtt_connect = MQTT_Connection("subscriber", weather_topics, weather_data_handler, "json")

# * ----------------------------------------------------- Landing Page Functionality -----------------------------------------------------
# * List of datahandler objects
dataHandlers = [weather_data_handler, wall_power_data_handler]

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
def generate_socket_events(socket_topic, data_handler):
    # * Socket_topics should be string or list of strings of topics to send the current state to
    if isinstance(socket_topic, str):
        # Convert single string to a list with a single element
        self_socket_topics = [socket_topic]
    elif isinstance(socket_topic, list):
        # Check all elements of the list are of type string before assigning
        if all(isinstance(s, str) for s in socket_topic):
            self_socket_topics = socket_topic
        else:
            raise TypeError(f"Error: All elements of socket_topic list must be strings. Received: {socket_topic}")
    else:
        raise TypeError("Error: topic must be a string or a list of strings")
    
    
    # * data_handler should be DataHandler or list of DataHandlers
    if isinstance(data_handler, DataHandler):
        # Convert single DataHandler to a list with a single element
        self_data_handler = [data_handler]
    elif isinstance(data_handler, list):
        # Check length of both data_handler and socket_topic match
        if (len(socket_topic) != len(data_handler)):
            raise TypeError(f"Error: Number of elements in data_handler must equal socket_topic:\n{data_handler}\n{socket_topic}")
            
        # Check all elements of the list are of type DataHandler before assigning
        if all(isinstance(DH, DataHandler) for DH in data_handler):
            self_data_handler = data_handler
        else:
            raise TypeError(f"Error: All elements of data_handler list must be type DataHandler. Received: {data_handler}")
    else:
        raise TypeError("Error: topic must be a DataHandler or a list of DataHandlers")
    
    # * Send data to connected clients
    for i in range(len(self_data_handler)):
        if self_data_handler[i].get_update_flag():
            self_data_handler[i].unset_update_flag()
            
            current_data = self_data_handler[i].get_current_data()
            
            # print(f"{socket_topic[i]}: {current_data}")
            socketio.emit(socket_topic[i], current_data)
        
socket_thread = None
socket_thread_lock = threading.Lock()

def background_thread():
    while True:
        generate_socket_events(['alert', 'weather', 'wall_power'], [alert_data_handler, weather_data_handler, wall_power_data_handler])
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
    
    # localhost button Section
    # * Reboot Button → /localhost/reboot → Reboot Raspberry Pi
    elif object == "localhost" and action == "reboot":
        subprocess.run(['sudo', 'reboot'])
        
    return redirect(url_for('main'))

# * ----------------------------------------------------- Host Local Website with Debugging Enabled -----------------------------------------------------
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=80, debug=debugFlag)