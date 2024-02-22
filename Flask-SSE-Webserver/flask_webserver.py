from flask import Flask, redirect, url_for, render_template, Response, jsonify
import time
import paho.mqtt.client as mqtt
import json
import copy
import threading


""" # * Commented out RPi.GPIO import for Windows compatibility
# import RPi.GPIO as GPIO

# * Commented out Raspberry Pi specific imports for Windows compatibility
# import time, picamera2
# from camera_still import Camera
# import ultrasonic, door_operation, limit_switch, camera_still

# * Commented out GPIO setup for Raspberry Pi
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)

# * Commented out Raspberry Pi GPIO setup code
# door_operation.door_motor_setup()
# limit_switch.lsw_setup(5)
# ultrasonic.ultrasonic_setup(26,6) """

app = Flask(__name__, template_folder='static')
# * ----------------------------------------------------- MQTT Events -----------------------------------------------------
""" # * Dictionary to store the incomming data from MQTT topics
currentData = {
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
    'New_Subsystem_Data' : {
        
    }
}

# Initialize previousData with None values
previousData = copy.deepcopy(currentData) """

class DataHandler:
    def __init__(self):
        self.current_data = {
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
            'New_Subsystem_Data': {}
        }
        self.previous_data = copy.deepcopy(self.current_data)
        self.lock = threading.Lock()

    def update_current_data(self, new_data):
        with self.lock:
            self.previous_data = self.current_data
            self.current_data = new_data

    def get_current_data(self):
        with self.lock:
            return self.current_data

data_handler = DataHandler()

# MQTT broker details
broker_address = "localhost"
port = 1883

# * Callback function for when a message is received
def on_message(client, userdata, msg):
    # Deserialize JSON data
    deserialized_data = json.loads(msg.payload)
    
    if msg.topic == "weather_topic":
        data_handler.update_current_data({'weather_data': deserialized_data})
        # currentData['weather_data'] = deserialized_data
        print("Updated weather_data.")

# Create MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set up message callback
client.on_message = on_message

# Connect to broker
client.connect(broker_address, port, 60)

# Subscribe to topic
client.subscribe("weather_topic")

# Start the MQTT client loop
client.loop_start()

# * ----------------------------------------------------- Server Sent Events -----------------------------------------------------
def generate_events():
   with app.app_context():
      while True:
        # * Simulate JSON data from microcontroller
        #  data = { "timestamp": time.time(), "value": 42 }
        current_data = data_handler.get_current_data()
         
        # * Convert the JSON data to a string and format as an SSE message
        if data_handler.previous_data != current_data:
            json_data = jsonify(current_data).get_data(as_text=True).replace('\n', '')
            sse_message = f"data: {json_data}\n\n"
        
            # * Yield the SSE message
            yield sse_message
            
            # * Wait for a brief interval before sending the next event
            time.sleep(1)
        
            #  * Update State
            # previousData = currentData

# * Route for SSE endpoint
@app.route('/events')
def events():
    # * Return a response with the SSE content type and the generator function
    return Response(generate_events(), content_type='text/event-stream')

# * ----------------------------------------------------- Landing Page Functionality -----------------------------------------------------
# * Redirect to index.html if trying to load root page.
@app.route("/")
def root():
    return redirect(url_for('main'))

@app.route("/index.html")
def main():
    return render_template('index.html')


# * ----------------------------------------------------- Control Modules -----------------------------------------------------
# * Dummy function to simulate camera frame captured
def dummy_camera_frame():
    # * This function would capture a frame from a camera (simulated here)
    # * Replace this with actual camera frame capture code on Windows PC
    return b'Dummy Camera Frame'

def gen():
    while True:
        frame = dummy_camera_frame()  # * Replace with actual camera frame capture function call
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# * Mock function to simulate ultrasonic distance measurement
def get_distance():
    # * This function would get distance from ultrasonic sensor (simulated here)
    # * Replace with actual distance measurement code on Windows PC
    return 10.0  # * Simulated distance value

@app.route("/<pin>/<action>")
def action(pin, action):
    distance = ''
    if pin == "pin1" and action == "on":
        dist = get_distance()  # * Replace with actual distance measurement function call
        dist = '{0:0.1f}'.format(dist)
        distance = dist

    # * Dummy print statements
    if pin == "door" and action == "open":
        print("door opened")

    if pin == "door" and action == "close":
        print("door closed")

    if pin == "camera" and action == "still":
        print("taking photos...")
        # * Dummy camera still capture
        # * Replace with actual camera capture code on Windows PC
        time.sleep(5)

    templateData = {
        'distance': distance,
    }
    return render_template('index.html', **templateData)

# * ----------------------------------------------------- Host Local Website with Debugging Enabled -----------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
