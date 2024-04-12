##############################################################################
#                                 Spot Interaction
# Talks with Spot API or Spot Collar to determine door operation
#
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##############################################################################

from classes import mqtt_connection
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

try:
    robot, id_client = robot_setup()
    robot_state_client = robot.ensure_client(RobotStateClient.default_service_name)
except:
    print("Spot robot not connected. Continuing with non-connected protocol...")

# * ------------------------------RSSI Connection-----------------------------------

last_rssi_state = "approaching"

def rssi_eval(rssi_value):
    global last_rssi_state
    if rssi_value > -50 and last_rssi_state == "leaving": #TODO callibrate these numbers                        
        mqtt_connect.publish('door', 'open')
        time.sleep(60)
    elif rssi_value < -80 and last_rssi_state == "approaching":
        mqtt_connect.publish('door', 'close')
        time.sleep(60)

def on_message_rssi(self, client, msg):
    if msg.topic == 'rssi':
        print(msg.payload)
        rssi_eval(int(msg.payload))

mqtt_connect = mqtt_connection.MQTT_Connection(type='both', topics = ['rssi'], on_message=on_message_rssi)

last_state = "not_charging"

while True:
    time.sleep(1)
    if Spot_API_Connect_Flag:
        state = robot_state_client.get_robot_state()
        mqtt_connect.publish('battery_state', str(state.battery_states[0].charge_percentage.value))

        if state.battery_states[0].current.value > 0 and last_state == "not_charging":   # pos - charging, neg - not
            mqtt_connect.publish('door', 'close')
            last_state = "charging"
        elif state.battery_states[0].current.value <= 0 and last_state == "charging":
            mqtt_connect.publish('door', 'open')
            last_state = "not_charging"




        