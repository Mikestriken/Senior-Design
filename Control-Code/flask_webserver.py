from flask import Flask, render_template, Response
import RPi.GPIO as GPIO

import time, picamera2

from camera_still import Camera

import ultrasonic, door_operation, limit_switch, camera_still

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#set up
door_operation.door_motor_setup()
limit_switch.lsw_setup(5)
ultrasonic.ultrasonic_setup(26,6)
 
app = Flask(__name__, template_folder = 'static')
 
# Default page
@app.route("/")
 
def main():
   return render_template('main2.html')   

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<pin>/<action>")
def action(pin, action):
   temperature = ''
   humidity = ''
   distance = ''

   if pin == "pin1" and action == "on":
      dist = ultrasonic.get_distance()
      dist = '{0:0.1f}' .format(dist)
      distance = dist
   
   if pin == "door" and action == "open":
      door_operation.open_door()
      print("door opened")

   if pin == "door" and action == "close":
      door_operation.close_door()
      print("door closed")

   if pin == "camera" and action == "still":
      print("taking photos...")
      camera_still.camera_setup()
      camera_still.take_still()
      camera_still.close_cam()
      time.sleep(5)


 
   templateData = {
   'distance' : distance,
   }
 
   return render_template('main2.html', **templateData)
 
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)