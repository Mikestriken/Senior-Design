from flask import Flask, render_template
import RPi.GPIO as GPIO

import ultrasonic
 
app = Flask(__name__)
 
GPIO.setmode(GPIO.BCM)
 
@app.route("/")
 
def main():
   return render_template('main.html')
 
# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<pin>/<action>")
def action(pin, action):
   temperature = ''
   humidity = ''
   if pin == "pin1" and action == "on":
      dist = ultrasonic.get_distance()
      dist = '{0:0.1f}' .format(dist)
      distance = 'Distance: ' + dist
   
 
   templateData = {
   'distance' : distance
   }
 
   return render_template('main.html', **templateData)
 
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)