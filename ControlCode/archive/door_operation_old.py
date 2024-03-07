##############################################################################
#                                 Door Operation
# TODO 
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
#
##############################################################################
import limit_switch, ultrasonic
import RPi.GPIO as GPIO
import time

IN1 = 23
IN2 = 24
ENA = 12 # pwm

DUTY_CYCLE = 25  # Linear actuator max is 25

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

GPIO.output(IN1, False)
GPIO.output(IN2, False)

PWMSet = GPIO.PWM(ENA, 500)
PWMSet.ChangeDutyCycle(DUTY_CYCLE)
PWMSet.start(0)

def door_collision_setup():
    limit_switch.lsw_setup(5)
    ultrasonic.ultrasonic_setup(26,6)

def open_door():
    #TODO

    GPIO.output(IN2, False)
    GPIO.output(IN1, True)
    
    time.sleep(10)

    GPIO.output(IN1, False)

    print("opening...")

def close_door():
    #TODO

    GPIO.output(IN1, False)
    GPIO.output(IN2, True)

    time.sleep(10)

    GPIO.output(IN2, False)

    print("closing...")

def stop_door():
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    print("door stopped")