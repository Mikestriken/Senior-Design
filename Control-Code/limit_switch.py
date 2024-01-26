import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO_NUMBER =  5

GPIO.setup(GPIO_NUMBER, GPIO.IN)

def limit_isr(self):
    print("Was Pressed!")

GPIO.add_event_detect(GPIO_NUMBER, GPIO.FALLING, 
    callback=limit_isr, bouncetime=300)

while 1:
    i = 1