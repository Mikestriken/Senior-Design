##############################################################################
#                                 Spot Interaction
# Talks with Spot API or Spot Collar to determine door operation
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##############################################################################

from classes import mqtt_connection
import json
import time

try:
    import bosdyn.client
    import bosdyn.client.util
    from bosdyn.client.robot_state import RobotStateClient
except:
    print("Bosdyn.client not installed")


Spot_API_Connect_Flag = 0
Ultrasonic_Close_Door_Flag = 1

# * ---------------------------Spot API Connection-------------------------------

def robot_setup():
    global Spot_API_Connect_Flag 

    sdk = bosdyn.client.create_standard_sdk('RobotStateClient')
    robot = sdk.create_robot('192.168.80.3')
    id_client = robot.ensure_client('robot-id')

    robot.authenticate('test-user', 'epri-spot123')

    robot.time_sync.wait_for_sync()

    Spot_API_Connect_Flag = 1

    return robot, id_client

def spot_rssi_operation(rssi):
    rssi = int(rssi)
    if rssi < -40:                                      #TODO callibrate this number
        mqtt_connect.publish('door', 'open')
    elif Spot_API_Connect_Flag:
        state = robot_state_client.get_robot_state()
        if (state.battery_states[0].current.value < 0): # pos - charging, neg - not
            mqtt_connect.publish('door', 'close')
    elif Ultrasonic_Close_Door_Flag:
        mqtt_connect.publish('door', 'close')


def on_message_main(msg):
        # Deserialize JSON data
        deserialized_data = json.loads(msg.payload)
        
        if msg.topic == 'rssi':
            spot_rssi_operation(msg.payload)

mqtt_connect = mqtt_connection.MQTT_Connection(type='both', topics = ['rssi'], on_message=on_message_main)

try:
    robot, id_client = robot_setup()
    robot_state_client = robot.ensure_client(RobotStateClient.default_service_name)
except:
    print("Spot robot not connected. Continuing with non-connected protocol...")

# * ------------------------------RSSI Connection-----------------------------------



def rssi_eval(rssi_value):
    if rssi_value < -80:                        #TODO callibrate these numbers
        mqtt_connect.publish('door', 'open')
    elif rssi_value > -60:
        mqtt_connect.publish('door', 'close')

def on_message_rssi(self, client, msg):
        # Deserialize JSON data
        #deserialized_data = json.loads(msg.payload)
        
        with open('/home/eprispot/Desktop/readme.txt', 'w') as f: #DEBUGGING
            f.write(msg.payload.decode("utf-8"))

        if msg.topic == 'rssi':
            print(msg.payload)
            rssi_eval(int(msg.payload))

rssi_mqtt = mqtt_connection.MQTT_Connection(type='both')


while True:
    time.sleep(1)
    if Spot_API_Connect_Flag:
        state = robot_state_client.get_robot_state()
        mqtt_connect.publishAsJSON('battery_state', state.battery_states[0].charge_percentage.value)
         # print(state.battery_states[0].current.value) # pos - charging, neg - not



        