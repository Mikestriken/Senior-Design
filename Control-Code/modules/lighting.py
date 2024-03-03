##############################################################################
#                                 Lighting TODO
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##############################################################################
import RPi.GPIO as GPIO

import schedule
import time

class Indoor_Lighting():
    def __init__(self, gpio_pin):
        GPIO.setup(gpio_pin, GPIO.OUT)

    def power_on(self):
        GPIO.output(self.gpio_pin, True)

    def power_off(self):
        GPIO.output(self.gpio_pin, False)

class Outdoor_Lighting():
    def __init__(self, gpio_pin):
        GPIO.setup(gpio_pin, GPIO.OUT)

    def power_on(self):
        GPIO.output(self.gpio_pin, True)

    def power_off(self):
        GPIO.output(self.gpio_pin, False)
    

    def your_task(self):
        # Your task code goes here
        self.power_on

    # Schedule the task at the sunrise time
    schedule.every().day.at(sunrise_time.strftime("%H:%M")).do(your_task)

    while True:
        schedule.run_pending()
        time.sleep(1)
