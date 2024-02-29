import RPi.GPIO as GPIO

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin
Power_Relay_Pin = 23

# Setup the GPIO pin as input with a pull-down resistor
GPIO.setup(Power_Relay_Pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

# Define the ISR function
def my_callback(channel):
    print("GPIO pin {} has changed from LOW to HIGH".format(channel))

# Add event detection to the GPIO pin
GPIO.add_event_detect(Power_Relay_Pin, GPIO.RISING, callback=my_callback, bouncetime=200)

try:
    print("Waiting for interrupt...")
    # Your main code can continue here while waiting for the interrupt
    while True:
        pass

except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    GPIO.cleanup()
