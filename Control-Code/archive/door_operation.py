##############################################################################
#                                 Door Operation
# TODO 
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
#
##############################################################################

import RPi.GPIO as GPIO
import time

def door_motor_setup():
    global IN1, IN2, ENA, DUTY_CYCLE

    IN1 = 23
    IN2 = 24
    ENA = 12 # pwm

    DUTY_CYCLE = 25  # Linear actuator max is 25

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)

    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(ENA, True)

    global PWMSet

    PWMSet = GPIO.PWM(ENA, 60)
    PWMSet.ChangeDutyCycle(DUTY_CYCLE)
    PWMSet.start(DUTY_CYCLE)

def stop_door():
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    print("door stopped!")

def test_funct():
    c_scale = [260, 293, 330, 350, 392, 440, 493, 523]

    for i in c_scale:
        PWMSet.ChangeFrequency(i)
        print("Changing Frequency to: "+ str(i))
        time.sleep(10)
    
    
    for i in [20, 30, 40, 50, 100, 50]:
        PWMSet.ChangeDutyCycle(i)
        print("Changing Duty Cycle to: "+ str(i))
        time.sleep(2)

def open_door():
    #TODO

    print("opening...")

    # Set IN1 -> 1, IN2 -> 0
    GPIO.output(IN2, False)
    GPIO.output(IN1, True)
    
    #test_funct()
    time.sleep(60)

    # Break and wait, IN1 -> 0, IN2 -> 0
    GPIO.output(IN1, False)
    time.sleep(1)

def close_door():
    #TODO

    print("closing...")

    # Set IN1 -> 0, IN2 -> 1
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    
    time.sleep(66)

    # Break and wait, IN1 -> 0, IN2 -> 0
    GPIO.output(IN2, False)
    time.sleep(1)
