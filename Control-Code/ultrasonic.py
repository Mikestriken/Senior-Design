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

SONIC_SPEED = 34300

GPIO.setmode(GPIO.BCM)  # BCM For GPIO numbering instead of pin numbering

GPIO_TRIGGER = 26       # Regular Pin
GPIO_ECHO = 6           # Regular Pin

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def trigger_pulse(trigger):
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, True)

def measure_time(echo):
    start = time.time()
    stop = time.time()

    while GPIO.input(echo) == 0:
        start = time.time()

    while GPIO.input(echo) == 1:
        stop = time.time()

    return stop - start

def distance_calc(time):
    return (time * SONIC_SPEED)/2

def get_distance():
    trigger_pulse(GPIO_TRIGGER)
    return distance_calc(measure_time())



