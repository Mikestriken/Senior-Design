##############################################################################
#                                 Lighting
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##############################################################################
import RPi.GPIO as GPIO

class Indoor_Lighting():
    def __init__(self, gpio_pin):
        GPIO.setup(gpio_pin, GPIO.OUT)

    def power_on(self):
        GPIO.output(self.gpio_pin, True)

    def power_off(self):
        GPIO.output(self.gpio_pin, False)
    
