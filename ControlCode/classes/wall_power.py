##################################################################################
#                                 Wall Power
#
# Created by Michael Marais and Joelle Bailey for EPRI_SPOT, Spring 2024
##################################################################################

import RPi.GPIO as GPIO

class Wall_Power():
    def __init__(self, gpio_pin = 22):
        
        GPIO.setmode(GPIO.BCM)
        
        self.gpio_pin = gpio_pin

        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    # * Pin High => No Wall Power (vice versa)
    def powerState(self):
        if GPIO.input(self.gpio_pin):
            return False
        else:
            return True
            
            
    def __del__(self):
        GPIO.cleanup()