import unittest
import ultrasonic

class UltraSonicTest(unittest.TestCase):
    def test(self):
        for reading in range(0,5):
            distance = ultrasonic.get_distance()
            print("Distance Reading #" + str(reading) + ": %.1f cm" % distance)


if __name__ == '__main__':
    unittest.main()
