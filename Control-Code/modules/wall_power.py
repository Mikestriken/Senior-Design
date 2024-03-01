##################################################################################
#                                 Wall Power
#
# Created by Michael Marais refactored by Joelle Bailey for EPRI_SPOT, Spring 2024
##################################################################################

import RPi.GPIO as GPIO

def my_callback(channel):
    print("GPIO pin {} has changed from LOW to HIGH".format(channel))

class Wall_Power():
    def __init__(self, wall_power_isr = my_callback, gpio_pin = 23):
        self.gpio_pin = gpio_pin

        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        # Add event detection to the GPIO pin
        GPIO.add_event_detect(self.gpio_pin, GPIO.RISING, callback=wall_power_isr, bouncetime=200)


