##############################################################################
#                                 Door Operation
# Door object and operation for motor controller and linear actuator interface
# has operations: open, close, stop door, self contained isr 
# 
# Inputs: in1, in2, ena, duty_cycle
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
#
##############################################################################

import RPi.GPIO as GPIO
import time


class Door:
    def __init__(self, in1 = 23, in2 = 24, ena = 12, duty_cycle = 25, pwm = 60):
        self.percent_open = 0
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
        print("opening...")

        # Set IN1 -> 1, IN2 -> 0
        GPIO.output(self.in1, True)
        GPIO.output(self.in2, False)

        while(self.percent_open < 100):
            time.sleep(0.15)
            self.percent_open += 1

        
        # Break and wait, IN1 -> 0, IN2 -> 0
        GPIO.output(self.in1, False)
        time.sleep(1)

    def close_door(self):
        print("closing...")

        # Set IN1 -> 0, IN2 -> 1
        GPIO.output(self.in1, False)
        GPIO.output(self.in2, True)
        
        while(self.percent_open > 0):
            time.sleep(0.17)
            self.percent_open -= 1

        # Break and wait, IN1 -> 0, IN2 -> 0
        GPIO.output(self.in2, False)
        time.sleep(1)
        
    def stop_door(self):
        GPIO.output(self.in1, False)
        GPIO.output(self.in2, False)
        print("door stopped! Percent Open: " + self.percent_open)

    def door_collision_isr(self, door):
        self.stop_door()
        print("collision detected")

    def get_percent_open(self):
        return self.percent_open
