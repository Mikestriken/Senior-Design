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

class Ultrasonic:
    # Enter BCM trigger and echo pin numbers 26, 6
    def __init__(self, trigger = 26, echo = 6):
        self.SONIC_SPEED = 34300
        self.trigger = trigger
        self.echo = echo

        GPIO.setmode(GPIO.BCM)  # BCM For GPIO numbering instead of pin numbering
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def trigger_pulse(self):
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)

    def measure_time(self):
        start = time.time()
        stop = time.time()

        count = 0

        while GPIO.input(self.echo) == 0:
            count = count + 1
            if count > 3000:
                break
            start = time.time()

        while GPIO.input(self.echo) == 1:
            stop = time.time()

        return stop - start

    def distance_calc(self, time):
        return (time * self.SONIC_SPEED)/2

    def get_distance(self):
        distance = -1
        while distance < 0:
            self.trigger_pulse()
            distance = self.distance_calc(self.measure_time())
        return distance
    
    def get_average_distance(self, num_readings):
        average = 0
        for _ in range(num_readings):
            distance = -1
            while distance < 0:
                self.trigger_pulse()
                distance = self.distance_calc(self.measure_time())
            average = (average + distance)/2
        return average



