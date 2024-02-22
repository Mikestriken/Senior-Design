##############################################################################
#                                 Limit
# Limit switch module
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
# dependant on door_operation.stop_door method
##############################################################################

import door_operation
import RPi.GPIO as GPIO

def limit_isr(self):
    door_operation.stop_door()
    print("collision detected")

def lsw_setup(pin_number):
    global GPIO_NUMBER
    GPIO_NUMBER = pin_number

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_NUMBER, GPIO.IN)

    GPIO.add_event_detect(GPIO_NUMBER, GPIO.FALLING, 
        callback=limit_isr, bouncetime=300)


        

    
