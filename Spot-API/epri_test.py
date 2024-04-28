##################################################################################
#                         EPRI Test Python Script
# This python script ...
# 
# Created by Joelle Bailey for EPRI_SPOT, Spring 2024
##################################################################################

import bosdyn.client
import bosdyn.client.util
from bosdyn.client.robot_state import RobotStateClient

# make an sdk object
sdk = bosdyn.client.create_standard_sdk('RobotStateClient')

robot = sdk.create_robot('192.168.80.3')

id_client = robot.ensure_client('robot-id')

robot.authenticate('test-user', 'epri-spot123')
#bosdyn.client.util.authenticate(robot)
robot.time_sync.wait_for_sync()

robot_state_client = robot.ensure_client(RobotStateClient.default_service_name)

state = robot_state_client.get_robot_state()

# print(state.battery_states[0].charge_percentage.value)
# print(state.battery_states[0].current.value) # pos - charging, neg - not

print(state)
