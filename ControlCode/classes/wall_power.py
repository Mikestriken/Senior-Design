##################################################################################
#                                 Wall Power
#
# Created by Michael Marais and Joelle Bailey for EPRI_SPOT, Spring 2024
#   * Relay Closes when Power is present.
#   * Pin High => Wall Power
#   * Pin Low => No Wall Power
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