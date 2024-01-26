import unittest
import ultrasonic

class UltraSonicTest(unittest.TestCase):
    def test(self):
        for reading in range(0,200):
            distance = ultrasonic.get_distance()
            print("Distance Reading #" + str(reading) + ": %.3f cm" % distance)


if __name__ == '__main__':
    unittest.main()
