##################################################################################
#                                 Wall Power
#
# Created by Michael Marais and Joelle Bailey for EPRI_SPOT, Spring 2024
##################################################################################

from classes.mqtt_connection import MQTT_Connection
from classes.wall_power import Wall_Power
import time
# * ----------------------------------------------------- Options and State Initialziation -----------------------------------------------------
# * Set to how long before sampling next state to determine if state has changed.
minutes_to_wait = 1

# * Init
wall_power = Wall_Power()
current_state = wall_power.powerState() # Get current state if we have power or not.
previous_state = current_state

# * ----------------------------------------------------- Helper Functions -----------------------------------------------------
# * Published "Wall Power Disconnected!" or "Wall Power Reconnected!" based on current state to MQTT topic `topic`
def publishCurrentState(topic):
    if current_state == False:
        mqtt_client.publish(topic, "Wall Power Disconnected!")
    else:
        mqtt_client.publish(topic, "Wall Power Reconnected!")
    

# * ----------------------------------------------------- MQTT Settings -----------------------------------------------------
# * Topic to return information on the wall power current state to on request
request_topic = "wall_power"

# * As soon as "update" is sent to the request_topic MQTT topic, this script will send publish the current state back to the same topic
def request_response(client, userdata, msg):
    try:
        if msg.payload.decode('utf-8').lower() == "update":
            publishCurrentState(topic=request_topic)
            
    except Exception as e:
        print(f"Something went Wrong...\nMessage: {msg.payload}\n\nError Log:")
        print(e)

# * MQTT client setup
mqtt_client = MQTT_Connection(type="both", topics=request_topic, data_handler=None, on_message_type="string", on_message=request_response)


# * ----------------------------------------------------- Main Loop -----------------------------------------------------
print("Wall Power Instantiated, listening...")

while True:
    # * Wait for minutes_to_wait...
    time.sleep(minutes_to_wait*60)
    
    # * Update Current State
    current_state = wall_power.powerState()
    
    # * Compare States, send alert if missmatch.
    if current_state != previous_state:
        publishCurrentState(topic="alert")
            
    # * Update State
    previous_state = current_state
    