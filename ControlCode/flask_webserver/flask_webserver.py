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
import json
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
# Note: Alert is its own topic because I want the alerts to be unbuffered. Alerts should take Priority.
                                                        # * Alert MQTT Client
# * Template for how the data should be formatted.
alert_template_data = {
            'alert': None
        }

# * MQTT topics to subscribe to
alert_topic = 'alert'

# * alert_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
alert_data_handler = DataHandler(alert_template_data)
alert_mqtt_connect = MQTT_Connection("subscriber", alert_topic, alert_data_handler, "string")

                                                        # * Big MQTT Client
# * Template for how the data should be formatted.
template_data = {
            'wall_power': "",
            'outdoor_weather': {
                'wind': {
                    'speed': "",
                    'rawDirection': "",
                    'trueDirection:': "",
                    'status': ""
                },
                'heading': "",
                'meteorological': {
                    'pressureMercury': "",
                    'pressureBars': "",
                    'temperature': "",
                    'humidity': "",
                    'dewPoint': ""
                }
            },
            'indoor_weather': {
                'temperature': "",
                'relative_humidity': ""
            },
            'battery_state': "",
            'door': "",
            'outdoor_light': "",
            'indoor_light': "",
            'fan': ""
        }

# * MQTT topics to subscribe to 
wall_power_topic = 'wall_power'
outdoor_weather_topic = 'outdoor_weather'
indoor_weather_topic = 'indoor_weather'
spot_battery_topic = 'battery_state'
door_topic = 'door'
outdoor_light_topic = 'outdoor_light'
indoor_light_topic = 'indoor_light'
fan_topic = 'fan'
topics = [wall_power_topic, outdoor_weather_topic, indoor_weather_topic, spot_battery_topic, door_topic, outdoor_light_topic, indoor_light_topic, fan_topic]

# * fan_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
data_handler = DataHandler(template_data)

# * Default, internal callback function for when a message is received
def on_message(client, userdata, msg):
    # * Find out which topic got a message and update the data_hander with the data.
    # print(f"New message: {msg.payload} → {msg.payload.decode('utf-8')}")
    try:
        # * Assign msg.payload to deserialized data appropriately
        deserialized_data = None
        
        # If msg.topic is associated with a dictionary in the template, load the message as a json type and check keys match before updating, 
        # else load deserialized_data as string.
        if (isinstance(template_data[msg.topic], dict)):
            deserialized_data = json.loads(msg.payload)
            
            if (deserialized_data.keys() == template_data[msg.topic].keys()): # If keys match, update current data.
                # Update the data_handler
                data_handler.update_current_data(msg.topic, deserialized_data)
                
                # print(f"Updated {msg.topic} with: {deserialized_data}\n")
                # print(data_handler.get_current_data())
        else:
            deserialized_data = str(msg.payload.decode('utf-8'))
        
        # * Message filtering and classification.
        if msg.topic == wall_power_topic: # Look for specific valid strings
            if (deserialized_data.lower() == "Wall Power Disconnected!".lower() or deserialized_data.lower() == "Wall Power Reconnected!".lower()):
                # Update the data_handler
                data_handler.update_current_data(msg.topic, deserialized_data)
                
                # print(f"Updated {msg.topic} with: {deserialized_data}\n")
                # print(data_handler.get_current_data())
            
        # Note 1: The `template_data[door]` property holds the current % the door is open.
        # Note 2: The client JS checks that template_data[door] is between 0 ↔ 100.
        elif msg.topic == spot_battery_topic or msg.topic == door_topic: # Look for values that can be interpreted as a number.
            try:
                # Attempt to cast deserialized_data as a float, if it fails, and exception will be thrown.
                float(deserialized_data)
                
                # Update the data_handler
                data_handler.update_current_data(msg.topic, deserialized_data)
                
                # print(f"Updated {msg.topic} with: {deserialized_data}\n")
                # print(data_handler.get_current_data())
                
            except ValueError:
                pass
                
        elif msg.topic == outdoor_light_topic or msg.topic == indoor_light_topic:
            if (deserialized_data.lower() == "is_off".lower() or deserialized_data.lower() == "is_on".lower()):
                # Update the data_handler
                data_handler.update_current_data(msg.topic, deserialized_data)
                
                # print(f"Updated {msg.topic} with: {deserialized_data}\n")
                # print(data_handler.get_current_data())
                
        elif msg.topic == fan_topic:
            if (deserialized_data.lower() == "is_off".lower() or deserialized_data.lower() == "is_slow".lower() or deserialized_data.lower() == "is_fast".lower()):
                # Update the data_handler
                data_handler.update_current_data(msg.topic, deserialized_data)
                
                # print(f"Updated {msg.topic} with: {deserialized_data}\n")
                # print(data_handler.get_current_data())
    except Exception as e:
        print(f"Something went Wrong...\nTopic: {msg.topic}\nMessage: {msg.payload}\n\nError Log:")
        print(e)

mqtt_connect = MQTT_Connection("both", topics, data_handler, on_message=on_message)

# * ----------------------------------------------------- Landing Page Functionality -----------------------------------------------------
# * Run code after a template has been rendered and response is about to be sent.
    # * This code sets the update flag, so that generate_socket_events will sent an update to the client.
    # * TL;DR This code syncs the client up whenever the client refreshes / loads the page.
@app.after_request
def after_request(response):
    data_handler.set_all_update_flags()
    
    return response

# * Redirect to index.html if trying to load root page.
@app.route("/")
def root():
    return redirect(url_for('main'))

@app.route("/index.html")
def main():
    return render_template('index.html')

# * ------------------------------------------ Web Sockets ------------------------------------------
def generate_socket_events(socket_topics, dataHandler):
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
    
    
    # * dataHandler should be DataHandler
    if not isinstance(dataHandler, DataHandler):
        raise TypeError("Error: dataHandler must be a DataHandler")
    
    # * Send data to connected clients
    for topic in socket_topics_list:
        if dataHandler.get_update_flag(topic):
            dataHandler.unset_update_flag(topic)
            
            current_data = dataHandler.get_current_data()
            
            # print(f"{topic}: {current_data[topic]}")
            socketio.emit(topic, current_data[topic])
        
socket_thread = None
socket_thread_lock = threading.Lock()

# * function to check that an 'object' doesn't have any properties or nested objects with value 'None'.
def check_none(obj):
    if obj == None:
        return True
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if v is None:
                return True
            if isinstance(v, dict):
                if check_none(v):
                    return True
    return False

def background_thread():
    topicsAwaitingFirstUpdate = [wall_power_topic, door_topic, outdoor_light_topic, indoor_light_topic, fan_topic]
    updatedList = [False] * len(topicsAwaitingFirstUpdate)
    updated = False
    
    while True:
        # * Set updated flag if everything in the updatedList is True
        if not updated:
            if all(updatedList):
                updated = True
                
            # * Update Updated List Flags
            for i in range(len(topicsAwaitingFirstUpdate)):
                # * Don't check for `None` if already updated.
                if updatedList[i] == True:
                    break
                
                # * Get current data
                current_data = data_handler.get_current_data()
                
                # * If topic in current_data is not none, set updatedList element to true
                if not check_none(current_data[topicsAwaitingFirstUpdate[i]]):
                    updatedList[i] = True
                
                # * Request an update
                mqtt_connect.publish(topicsAwaitingFirstUpdate[i], "query_state")
            
        generate_socket_events([alert_topic], alert_data_handler)
        generate_socket_events(topics, data_handler)
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
@app.route("/<object>/<action>")
def action(object, action):
    print("Action Called")
    # MQTT Section
    # * Open Button  → /openButton/click  → openButton,  "click"
    # * Close Button → /closeButton/click → closeButton, "click"
    if object == "openButton" or object == "closeButton":
        mqtt_connect.publish(object, action)
        
    # * Fan slider position change to: 0/1/2 => set speed to: stop/slow/fast
    elif object == "fanSlider":
        if action == '0':
            mqtt_connect.publish(fan_topic, "stop")
        elif action == '1':
            mqtt_connect.publish(fan_topic, "slow")
        elif action == '2':
            mqtt_connect.publish(fan_topic, "fast")
        
    # * light slider position change to: 0/1 => set to: on/off
    elif object == "indoorLightSlider":
        if action == '0':
            mqtt_connect.publish(indoor_light_topic, "off")
        elif action == '1':
            mqtt_connect.publish(indoor_light_topic, "on")
        
    # * light slider position change to: 0/1 => set to: on/off
    elif object == "outdoorLightSlider":
        if action == '0':
            mqtt_connect.publish(outdoor_light_topic, "off")
        elif action == '1':
            mqtt_connect.publish(outdoor_light_topic, "on")
    
    # localhost button Section
    # * Reboot Button → /localhost/reboot → Reboot Raspberry Pi
    elif object == "localhost" and action == "reboot":
        subprocess.run(['sudo', 'reboot'])
        
    return redirect(url_for('main'))

# * ----------------------------------------------------- Host Local Website with Debugging Enabled -----------------------------------------------------
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=80, debug=debugFlag)