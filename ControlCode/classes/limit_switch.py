##############################################################################
#                       Limit Switch Class Python Script
# The purpose of this python script is to define the GPIO to access the
# limit switches embedded in the door.
# 
# NOTE: THIS CODE IS NOW OBSOLETE AS THE LIMIT SWITCHES DID NOT WORK AS INTENDED.
# 
# The operation / main loop this script is tied to is found in
# /ControlCode/operations/door_operation.py
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##############################################################################

import RPi.GPIO as GPIO

class LimitSwitch:
    def __init__(self, limit_isr, pin_number = 5):
        self.pin_number = pin_number

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_number, GPIO.IN)

        GPIO.add_event_detect(self.pin_number, GPIO.FALLING, pull_up_down=GPIO.PUD_DOWN,
            callback=limit_isr, bouncetime=300)