##############################################################################
#                                 Blink
# Simple use case of pigpio for the flashing of a connected LED on GPIO 1.
# Flashes every one second for one second.
#
# Created by Joelle Bailey for EPRI_SPOT, Fall 2023
##############################################################################


# imports
import pigpio
import time

# setup
pi = pigpio.pi()       # initializes connection
pi.set_mode(1, pigpio.OUTPUT)   # GPIO 1 to out

# functionality
pi.write(1,1)

for i in range(0,1000):
    if i%2:
        pi.write(1, 1)
    else:
        pi.write(1, 0)
    time.sleep(1)


