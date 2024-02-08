##############################################################################
#                                 Ultrasonic
# Ultrasonic sensor operation HC-SR04, returns distance in cm 
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
# with the help of tutorial:
# https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
##############################################################################

import RPi.GPIO as GPIO
import time

# Enter BCM trigger and echo pin numbers 26, 6
def ultrasonic_setup(trigger, echo):
    global SONIC_SPEED, GPIO_TRIGGER, GPIO_ECHO

    SONIC_SPEED = 34300
    GPIO_TRIGGER = trigger
    GPIO_ECHO = echo

    GPIO.setmode(GPIO.BCM)  # BCM For GPIO numbering instead of pin numbering
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

def trigger_pulse(trigger):
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

def measure_time(echo):
    start = time.time()
    stop = time.time()

    count = 0

    while GPIO.input(echo) == 0:
        count = count + 1
        if count > 3000:
            break
        start = time.time()

    while GPIO.input(echo) == 1:
        stop = time.time()

    return stop - start

def distance_calc(time):
    return (time * SONIC_SPEED)/2

def get_distance():
    distance = -1
    while distance < 0:
        trigger_pulse(GPIO_TRIGGER)
        distance = distance_calc(measure_time(GPIO_ECHO))
    return distance



