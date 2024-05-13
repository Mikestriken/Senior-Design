##############################################################################
#           Motor Current Threshold Detection Class Python Script
# The purpose of this python script is to define the GPIO necessary to access
# the DC current sensor.
# 
# The operation / main loop this script is tied to is found in
# /ControlCode/operations/door_operation.py
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##############################################################################

import RPi.GPIO as GPIO

class MotorCurrent:
    def __init__(self, isr, pin_number = 18):
        self.pin_number = pin_number

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.pin_number, GPIO.RISING,
            callback=isr, bouncetime=300)