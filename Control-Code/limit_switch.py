import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO_NUMBER =  5

GPIO.setup(GPIO_NUMBER, GPIO.IN)

def limit_isr():
    print(str(GPIO.input(GPIO_NUMBER)))

while GPIO.input(GPIO_NUMBER) == 0:
    start = time.time()

GPIO.add_event_detect(GPIO_NUMBER, GPIO.FALLING, 
    callback=limit_isr, bouncetime=100)

