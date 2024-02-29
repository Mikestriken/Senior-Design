##############################################################################
#                                 Limit
# Limit switch module
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##############################################################################

import RPi.GPIO as GPIO

class LimitSwitch:
    def __init__(self, limit_isr, pin_number = 5):
        self.pin_number = pin_number

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_number, GPIO.IN)

        GPIO.add_event_detect(self.pin_number, GPIO.FALLING, 
            callback=limit_isr, bouncetime=300)



        

    
