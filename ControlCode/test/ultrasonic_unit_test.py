import unittest
from classes import ultrasonic
from RPi import GPIO

#GPIO.cleanup()

sensor = ultrasonic.Ultrasonic()

class UltraSonicTest(unittest.TestCase):
    def test(self):
        for reading in range(0,200):
            distance = sensor.get_distance()
            print("Distance Reading #" + str(reading) + ": %.3f cm" % distance)


""" if __name__ == '__main__':
    unittest.main() """

for reading in range(0,200):
    distance = sensor.get_distance()
    print("Distance Reading #" + str(reading) + ": %.3f cm" % distance)