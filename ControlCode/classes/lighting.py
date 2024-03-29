##############################################################################
#                                 Lighting TODO
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##############################################################################
import RPi.GPIO as GPIO


class Indoor_Lighting():
    def __init__(self, gpio_pin = 27):
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

