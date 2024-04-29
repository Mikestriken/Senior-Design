##############################################################################
#                      Fan Class Python Script
# This python script defines the GPIO configuration for the fan used used
# to control the internal temperature of the docking station.
# 
# The operation / main loop this script is tied to is found in
# /ControlCode/operations/fan_operation.py
#
# Created by Joelle Bailey, Spring 2024
##############################################################################

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Fan():
    def __init__(self, gpio_pin = 25, speed_pin = 8):
        self.gpio_pin = gpio_pin
        self.speed_pin = speed_pin
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.setup(self.speed_pin, GPIO.OUT)

        GPIO.output(self.speed_pin, False)
        GPIO.output(self.gpio_pin, False)

        self.is_on = False
        self.is_fast = False
        self.power_on()

    def power_on(self):
        GPIO.output(self.gpio_pin, True)
        GPIO.output(self.speed_pin, False)
        self.is_on = True
        self.is_fast = True

    def speed_low(self):
        GPIO.output(self.gpio_pin, True)
        GPIO.output(self.speed_pin, True)
        self.is_fast = False
        
    def power_off(self):
        GPIO.output(self.gpio_pin, False)
        GPIO.output(self.speed_pin, False)
        self.is_on = False
        self.is_fast = False

    def toggle(self):
        if self.is_on:
            self.power_off
        else:
            self.power_on

    def get_state(self):
        return self.is_on, self.is_fast