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
import sys
import socket
import subprocess

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

                                                        # * Weather MQTT
# * Template for how the data should be formatted.
weather_template_data = {
            'weather_topic': {
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
            'indoor_weather_topic': {
                'temperature' : None,
                'relative_humidity' : None
            }
        }

# * MQTT topics to subscribe to that will update the states.
weather_topics = ['weather_topic', 'indoor_weather_topic']

# * weather_data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
weather_data_handler = DataHandler(weather_template_data)
weather_mqtt_connect = MQTT_Connection("subscriber", weather_topics, weather_data_handler, "json")

# * ----------------------------------------------------- Landing Page Functionality -----------------------------------------------------
# * Redirect to index.html if trying to load root page.
@app.route("/")
def root():
    return redirect(url_for('main'))

@app.route("/index.html")
def main():
    return render_template('index.html')

# * ----------------------------------------------------- Server Sent Events -----------------------------------------------------
def generate_events(data_handler):
   with app.app_context():
      while True:
        # * Convert the JSON data to a string and format as an SSE message
        if data_handler.get_update_flag():
            data_handler.unset_update_flag()
            
            current_data = data_handler.get_current_data()
            
            # print(f"sending {current_data.heading}\n\n")
            
            json_data = jsonify(**current_data).get_data(as_text=True).replace('\n', '')
            
            # print(f"as {json_data}\n\n")
            
            sse_message = f"data: {json_data}\n\n"
        
            # * Yield the SSE message
            yield sse_message
         
        # * Wait for a brief interval before sending the next event
        time.sleep(1)

# * Route for SSE Weather endpoint
@app.route('/weather-events')
def weather_events():
    # * Return a response with the SSE content type and the generator function
    return Response(generate_events(weather_data_handler), content_type='text/event-stream')

# * Route for SSE Weather endpoint
@app.route('/alert-events')
def alert_events():
    # * Return a response with the SSE content type and the generator function
    return Response(generate_events(alert_data_handler), content_type='text/event-stream')

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
    # * Open Button  → /openButton/click  → openButton_topic,  "click"
    # * Close Button → /closeButton/click → closeButton_topic, "click"
    door_mqtt_connect.publish(object + "_topic", action)
        
    return redirect(url_for('main'))

                    # localhost Buttons
door_mqtt_connect = MQTT_Connection("publisher")

@app.route("/localhost/<action>")
def action(action):
    # * Terminal Button  → /localhost/terminal  → Open Terminal
    # * Reboot Button → /localhost/reboot → Reboot Raspberry Pi
    if action == "terminal":
        subprocess.Popen(["lxterminal"])
        
    elif action == "reboot":
        subprocess.run(['sudo', 'reboot'])
        
    return redirect(url_for('main'))

# * ----------------------------------------------------- Host Local Website with Debugging Enabled -----------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=debugFlag)
