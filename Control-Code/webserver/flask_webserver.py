##############################################################################
#                                 Flask Web Server
#
# Created by Joelle Bailey, Michael Marais for EPRI_SPOT, Spring 2024
##############################################################################

# webserver imports
from flask import Flask, redirect, url_for, render_template, Response, jsonify

# camera imports
import time
import picamera2, cv2
import indoor_camera, outdoor_camera


app = Flask(__name__, template_folder='static')

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
         # * Simulate JSON data from microcontroller
         #indoor_temperature, indoor_relative_humidity = sht.measurements

         data = { "timestamp": time.time(), "value": 42, "indoor_temperature": 1, "indoor_humidity": 1 }
         
         # * Convert the JSON data to a string and format as an SSE message
         json_data = jsonify(data).get_data(as_text=True).replace('\n', '')
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


@app.route("/<pin>/<action>")
def action(pin, action):
    distance = ''
    if pin == "pin1" and action == "on":
        dist = 18
        dist = '{0:0.1f}'.format(dist)
        distance = dist

    # * Dummy print statements
    if pin == "door" and action == "open":
        print("door opened")

    if pin == "door" and action == "close":
        print("door closed")

    if pin == "camera" and action == "still":
        print()

    templateData = {
        'distance': distance,
    }
    return render_template('index.html', **templateData)

# * ----------------------------------------------------- Host Local Website with Debugging Enabled -----------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
