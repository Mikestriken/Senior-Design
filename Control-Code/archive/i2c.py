##############################################################################
#                                 I2C
# I2C implementation for the Raspberry Pi using pigpio.
# One byte send and receive.
#
# Created by Joelle Bailey for EPRI_SPOT, Fall 2023
##############################################################################

# imports
import pigpio
import time

# setup
pi = pigpio.pi()       # initializes connection

bus = 1             # Bus 0 or bus 1
address = 0x5C      # Device address, found in datasheet


# functionality

device = pi.i2c_open(bus, address)

pi.i2c_write_byte(device, 42)   # send byte 42 to device

b = pi.i2c_read_byte(device) # read a byte from device

print(b) #S Addr Rd [A] [Data] NA P
