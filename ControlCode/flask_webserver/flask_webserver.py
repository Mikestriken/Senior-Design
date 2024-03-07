##############################################################################
#                                 Flask Web Server
#
# Created by Joelle Bailey, Michael Marais for EPRI_SPOT, Spring 2024
#
# to run webserver:  python -B -m flask_webserver.flask_webserver
##############################################################################


from classes.data_handler import DataHandler
from classes.mqtt_connection import MQTT_Connection
import sys


# webserver imports
from flask import Flask, redirect, url_for, render_template, Response, jsonify

# * flag to remove camera code via command-line using --no-camera
cameraCodeFlag = True
if "--no-camera" in sys.argv:
    cameraCodeFlag = False
    
# * flag to enable debugging via command-line using --debug
debugFlag = False
if "--debug" in sys.argv:
    debugFlag = True

# camera imports
import time
if cameraCodeFlag:
    import indoor_camera, outdoor_camera

app = Flask(__name__, template_folder='static')

# * ----------------------------------------------------- MQTT and state storage -----------------------------------------------------
# * Template for how the data should be formatted.
template_data = {
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
                'temperature' : "...",
                'relative_humidity' : "..."
            }
        }

# * MQTT topics to subscribe to that will update the states.
webserver_topics = ['weather_topic', 'indoor_weather_topic', 'alert']

# * data_handler stores the states and also locks the storage to ensure multiple threads don't access at the same time.
data_handler = DataHandler(template_data)
mqtt_connect = MQTT_Connection("both", webserver_topics, data_handler)

# * ----------------------------------------------------- Landing Page Functionality -----------------------------------------------------
# * Redirect to index.html if trying to load root page.
@app.route("/")
def root():
    return redirect(url_for('main'))

@app.route("/index.html")
def main():
    return render_template('index.html')
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

# * ----------------------------------------------------- Server Sent Events -----------------------------------------------------
def generate_events():
   with app.app_context():
      while True:
        current_data = data_handler.get_current_data()
         
        # * Convert the JSON data to a string and format as an SSE message
        if data_handler.previous_data != current_data:
            # print(f"sending {current_data.heading}\n\n")
            json_data = jsonify(**current_data).get_data(as_text=True).replace('\n', '')
            # print(f"as {json_data}\n\n")
            sse_message = f"data: {json_data}\n\n"
        
            # * Yield the SSE message
            yield sse_message
         
        # * Wait for a brief interval before sending the next event
        time.sleep(1)

# * Route for SSE endpoint
@app.route('/events')
def events():
    # * Return a response with the SSE content type and the generator function
    return Response(generate_events(), content_type='text/event-stream')

# * ----------------------- Control Modules ------------------------------------------

if cameraCodeFlag:
    @app.route('/indoor_video_feed')
    def indoor_video_feed():
        return Response(gen(indoor_camera.Camera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/outdoor_video_feed')
    def outdoor_video_feed():
        return Response(gen2(outdoor_camera.Camera_outdoor()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        #return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


    @app.route("/<object>/<action>")
    def action(object, action):
        mqtt_connect.publishAsJSON(object, action)
        return redirect(url_for('main'))

# * ----------------------------------------------------- Host Local Website with Debugging Enabled -----------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=debugFlag)
