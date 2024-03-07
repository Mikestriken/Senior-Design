##################################################################################
#                                 Wall Power
#
# Created by Michael Marais and Joelle Bailey for EPRI_SPOT, Spring 2024
##################################################################################

from classes import mqtt_connection
import RPi.GPIO as GPIO

class Wall_Power():
    def __init__(self, wall_power_isr, mqtt_client = mqtt_connection.MQTT_Connection(), gpio_pin = 23):
        self.gpio_pin = gpio_pin
        self.mqtt_client = mqtt_client

        def callback(mqtt_client):
            mqtt_client.publish('alert', 'Wall Power Disconnected')

        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        # Add event detection to the GPIO pin
        GPIO.add_event_detect(self.gpio_pin, GPIO.RISING, callback=callback, bouncetime=200)



