##############################################################################
#                                 Flask Web Server
#
# Created by Joelle Bailey, Michael Marais for EPRI_SPOT, Spring 2024
##############################################################################

# webserver imports
from flask import Flask, redirect, url_for, render_template, Response, jsonify

import json
import data_handler
import mqtt_connection

# camera imports
import time
import indoor_camera, outdoor_camera

app = Flask(__name__, template_folder='static')

template_data = {
            'weather_data': {
                'wind': {
                    'speed': "TBD",
                    'direction': "TBD",
                    'status': "TBD"
                },
                'heading': "TBD",
                'meteorological': {
                    'pressureMercury': "TBD",
                    'pressureBars': "TBD",
                    'temperature': "TBD",
                    'humidity' : "TBD",
                    'dewPoint': "TBD"
                }
            },
            'indoor_weather': {
                'temperature' : "TBD",
                'relative_humidity' : "TBD"
            }
        }

webserver_topics = ['weather_data', 'indoor_weather']

data_handler = data_handler.DataHandler(template_data)
mqtt_connect = mqtt_connection.MQTT_Connection(data_handler, topics=webserver_topics)

# * ----------------------------------------------------- Landing Page Functionality -----------------------------------------------------
# * Redirect to index.html if trying to load root page.
@app.route("/")
def root():
    return redirect(url_for('main'))

@app.route("/index.html")
def main():
    return render_template('index.html')

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
            json_data = jsonify(current_data).get_data(as_text=True).replace('\n', '')
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
    mqtt_connect.publish(object, action)
    return redirect(url_for('main'))

# * ----------------------------------------------------- Host Local Website with Debugging Enabled -----------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
