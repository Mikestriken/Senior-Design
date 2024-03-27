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
minutes_to_wait = .1

# * Init
wall_power = Wall_Power()
current_state = wall_power.powerState() # Get current state if we have power or not.
previous_state = current_state

# * ----------------------------------------------------- Helper Functions -----------------------------------------------------
# * Published "Wall Power Disconnected!" or "Wall Power Reconnected!" based on current state to MQTT topic `topic`
def publishCurrentState(topics):
    # * Topics should be string or list of strings of topics to send the current state to
    if isinstance(topics, str):
        # Convert single string to a list with a single element
        selfTopics = [topics]
    elif isinstance(topics, list):
        # Check all elements of the list are of type string before assigning
        if all(isinstance(s, str) for s in topics):
            selfTopics = topics
        else:
            raise TypeError(f"All elements of topic list must be strings. Received: {topics}")
    else:
        raise TypeError("topic must be a string or a list of strings")
    
    # * Publish to all the topics
    if current_state == False:
        for topic in selfTopics:
            print(f"To: {topic}")
            mqtt_client.publish(topic, "Wall Power Disconnected!")
    else:
        for topic in selfTopics:
            print(f"To: {topic}")
            mqtt_client.publish(topic, "Wall Power Reconnected!")
    

# * ----------------------------------------------------- MQTT Settings -----------------------------------------------------
# * Topic to return information on the wall power current state to on request
wall_power_topic = "wall_power"

# * As soon as "update" is sent to the wall_power_request MQTT topic, this script will send publish the current state back to the same topic
def request_response(client, userdata, msg):
    try:
        if msg.payload.decode('utf-8').lower() == "query_state":
            publishCurrentState(topics=wall_power_topic)
            
    except Exception as e:
        print(f"Something went Wrong...\nMessage: {msg.payload}\n\nError Log:")
        print(e)

# * MQTT client setup
mqtt_client = MQTT_Connection(type="both", topics=wall_power_topic, data_handler=None, on_message_type="string", on_message=request_response)


# * ----------------------------------------------------- Main Loop -----------------------------------------------------
print("Wall Power Instantiated, listening...")

while True:
    # * Wait for minutes_to_wait...
    time.sleep(minutes_to_wait*60)
    
    # * Update Current State
    current_state = wall_power.powerState()
    
    # * Compare States, send alert if missmatch.
    if current_state != previous_state:
        publishCurrentState(topics=["alert", wall_power_topic])
            
    # * Update State
    previous_state = current_state
    