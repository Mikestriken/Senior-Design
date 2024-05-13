##############################################################################
#                      lighting Class Python Script
# This python script defines the GPIO configuration for the internal lighting
# of the dock house.
# 
# The operation / main loop this script is tied to is found in
# /ControlCode/operations/lighting_operation.py
#
# Created by Joelle Bailey, Spring 2024
# Commented by Michael Marais, Spring 2024
##############################################################################

import RPi.GPIO as GPIO

class Indoor_Lighting():
    def __init__(self, gpio_pin = 27):
        self.gpio_pin = gpio_pin
        GPIO.setup(gpio_pin, GPIO.OUT)
        self.is_on = False
        
        # * Turn on the light on start
        self.power_on()

    def power_on(self):
        GPIO.output(self.gpio_pin, True)
        self.is_on = True

    def power_off(self):
        GPIO.output(self.gpio_pin, False)
        self.is_on = False

    def toggle(self):
        if self.is_on:
            self.power_off
        else:
            self.power_on

# ! Outdoor lighting is obsolete. The Outdoor light is not controlled by the Raspberry Pi.
class Outdoor_Lighting():
    def __init__(self, gpio_pin = 4):
        self.gpio_pin = gpio_pin
        GPIO.setup(gpio_pin, GPIO.OUT)
        self.is_on = False
        self.power_on()

    def power_on(self):
        GPIO.output(self.gpio_pin, True)
        self.is_on = True

    def power_off(self):
        GPIO.output(self.gpio_pin, False)
        self.is_on = False

    def toggle(self):
        if self.is_on:
            self.power_off
        else:
            self.power_on

