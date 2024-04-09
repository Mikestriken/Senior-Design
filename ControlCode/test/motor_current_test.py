import RPi.GPIO as GPIO
import time

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin you want to read from
input_pin = 18

# Set up the pin as input
GPIO.setup(input_pin, GPIO.IN)

try:
    while True:
        # Read the input state
        input_state = GPIO.input(input_pin)
        
        # Print the input state
        print("Input state:", input_state)
        
        # Wait for a short duration
        time.sleep(0.1)  # Polling frequency

except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    GPIO.cleanup()