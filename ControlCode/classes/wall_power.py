##################################################################################
#                         Wall Power Class Python Script
# The purpose of this python script is to define the GPIO necessary to access
# the AC Current detection relay.
# 
# The relay closes when power is present:
#   * Pin High => Wall Power
#   * Pin Low => No Wall Power
# 
# The operation / main loop this script is tied to is found in
# /ControlCode/operations/wall_power_main.py
#
# Created by Michael Marais and Joelle Bailey for EPRI_SPOT, Spring 2024
##################################################################################

import RPi.GPIO as GPIO

class Wall_Power():
    def __init__(self, gpio_pin = 22):
        
        GPIO.setmode(GPIO.BCM)
        
        self.gpio_pin = gpio_pin

        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def powerState(self):
        if GPIO.input(self.gpio_pin):
            return True
        else:
            return False
            
            
    def __del__(self):
        GPIO.cleanup()