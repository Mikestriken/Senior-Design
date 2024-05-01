##############################################################################
#                              Door Class Python Script
# This script defines the Door object and operation for motor controller and
# linear actuator interface.
# 
# It has operations: open, close, stop door, self contained isr 
# 
# Inputs: in1, in2, ena, duty_cycle
# 
# The operation / main loop this script is tied to is found in
# /ControlCode/operations/door_operation.py
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##############################################################################

import RPi.GPIO as GPIO
import time
import os
import fcntl

from classes import mqtt_connection

GPIO.setwarnings(False)

class Door:
    def __init__(self, in1 = 23, in2 = 24, ena = 12, duty_cycle = 25, pwm = 60):
        # * Attempt to open the door_open_percent.txt file and read in data. If fail
        try:
            self.percent_open = self.get_percent_open()
        except:
            self.percent_open = 0
            print('Door Read Error, watch door for over-open')

        # * Init GPIO
        self.in1 = in1
        self.in2 = in2
        self.ena = ena
        self.duty_cycle = duty_cycle

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.ena, GPIO.OUT)

        GPIO.output(self.in1, False)
        GPIO.output(self.in2, False)
        GPIO.output(self.ena, True)

        self.PWMSet = GPIO.PWM(self.ena, pwm)
        self.PWMSet.ChangeDutyCycle(self.duty_cycle)
        self.PWMSet.start(self.duty_cycle)

    def test_funct(self):
        c_scale = [260, 293, 330, 350, 392, 440, 493, 523]
        
        sandstorm = [440, 493, 493, 493, 493, 493, 523, 493, 493, 493, 493, 493, 659, 659, 659, 587, 587, 587, 440, 493, 493, 493, 493, 493, 659, 493, 493, 493, 493, 493, 659, 659, 659, 587, 587, 587, 440, 493, 493, 493, 493, 493, 659, 493, 493, 493, 493, 493, 659, 987]

        for i in sandstorm:
            self.PWMSet.ChangeFrequency(i)
            print("Changing Frequency to: "+ str(i))
            time.sleep(2)
            
    def open_door(self):

        self.stop_door()

        print("opening...")
        self.percent_open = self.get_percent_open()

        # Set IN1 -> 1, IN2 -> 0
        GPIO.output(self.in2, False)
        GPIO.output(self.in1, True)

        while(self.percent_open < 100):
            time.sleep(0.20)
            self.percent_open += 1
            self.write_percent_open()

        
        # Break and wait, IN1 -> 0, IN2 -> 0
        GPIO.output(self.in1, False)
        print('opened')
        time.sleep(1)

    def close_door(self):

        self.stop_door()

        print("closing...")
        self.percent_open = self.get_percent_open()

        # Set IN1 -> 0, IN2 -> 1
        GPIO.output(self.in1, False)
        GPIO.output(self.in2, True)
        
        while(self.percent_open > 0):
            time.sleep(0.25)
            self.percent_open -= 1
            self.write_percent_open()

        if self.percent_open == 0:
            # Close the door for longer duration
            print("Closing door for longer duration...")
            time.sleep(10)  # Adjust the duration as needed

        # Break and wait, IN1 -> 0, IN2 -> 0
        GPIO.output(self.in2, False)
        print('closed')
        time.sleep(1)

    def open_door_multithreading(self, exit_event, percent_publisher):
        percent_publisher = mqtt_connection.MQTT_Connection("publisher")
        self.stop_door()
        
        print("opening...")
        self.percent_open = self.get_percent_open()

        # Set IN1 -> 1, IN2 -> 0
        GPIO.output(self.in1, True)
        GPIO.output(self.in2, False)

        while(self.percent_open < 100 and not exit_event.is_set()):
            time.sleep(0.20)
            self.percent_open += 1
            self.write_percent_open()
            percent_publisher.publish('door', str(self.percent_open))
        
        # Break and wait, IN1 -> 0, IN2 -> 0
        GPIO.output(self.in1, False)
        if not exit_event.is_set():
            print('opened')
        time.sleep(1)

    def close_door_multithreading(self, exit_event, percent_publisher):
        percent_publisher = mqtt_connection.MQTT_Connection("publisher")
        self.stop_door()

        print("closing...")
        self.percent_open = self.get_percent_open()

        # Set IN1 -> 0, IN2 -> 1
        GPIO.output(self.in1, False)
        GPIO.output(self.in2, True)
        
        while(self.percent_open > 0 and not exit_event.is_set()):
            time.sleep(0.25)
            self.percent_open -= 1
            self.write_percent_open()
            percent_publisher.publish('door', str(self.percent_open))

        if self.percent_open == 0:
            # Close the door for longer duration
            print("Closing door for longer duration...")
            time.sleep(10)  # Adjust the duration as needed

        # Break and wait, IN1 -> 0, IN2 -> 0
        GPIO.output(self.in2, False)
        if not exit_event.is_set():
            print('closed')
        time.sleep(1)
        
    def stop_door(self):
        GPIO.output(self.in1, False)
        GPIO.output(self.in2, False)
        print("door stopped! Percent Open: " + str(self.percent_open))

    def get_percent_open(self):
        script_dir = os.path.dirname(__file__)

        with open(script_dir + '/data/door_open_percent.txt') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            self.percent_open = int(f.read())
            fcntl.flock(f, fcntl.LOCK_UN)

        return self.percent_open

    def write_percent_open(self):
        #self.send_percent_open.publish('door', "this is a test") #TODO debug this, not printing out, on different thread?
        script_dir = os.path.dirname(__file__)
        with open(script_dir + '/data/door_open_percent.txt', 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(str(self.percent_open))
            fcntl.flock(f, fcntl.LOCK_UN)
