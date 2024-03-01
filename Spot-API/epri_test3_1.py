import bosdyn.client
import bosdyn.client.util
from bosdyn.client.robot_state import RobotStateClient

from bosdyn.client.docking import DockingClient
from bosdyn.client.graph_nav import GraphNavClient

def robot_setup():
    robot = sdk.create_robot('192.168.80.3')

    id_client = robot.ensure_client('robot-id')

    robot.authenticate('test-user', 'epri-spot123')

    robot.time_sync.wait_for_sync()

    return robot, id_client

##############
test = 0
##############

if test == 0:
    # make an sdk object
    sdk = bosdyn.client.create_standard_sdk('RobotStateClient')

    robot, id_client = robot_setup()

    robot_state_client = robot.ensure_client(RobotStateClient.default_service_name)

    state = robot_state_client.get_robot_state()

    # print(state.battery_states[0].charge_percentage.value)
    # print(state.battery_states[0].current.value) # pos - charging, neg - not
    print(state)

    with open('test0_state.txt', 'w') as file:
        file.write(state)


elif test == 1:
    sdk = bosdyn.client.create_standard_sdk('DockingClient')
    robot, id_client = robot_setup()

    docking_client = robot.ensure_client(DockingClient.default_service_name)

    state = docking_client.get_docking_state()
    dock_id = docking_client.get_dock_id()
    # .docking_command_feedback requires the command id from the dock issue request

    print(state)
    print(dock_id) # none if not docked

    with open('test1_docking.txt', 'w') as file:
        file.write(state)


elif test == 2:
    sdk = bosdyn.client.create_standard_sdk('GraphNavClient')
    robot, id_client = robot_setup()

    graph_nav_client = robot.ensure_client(GraphNavClient.default_service_name)

    state = graph_nav_client.get_localization_state(request_live_robot_state = True)

    gps = graph_nav_client.get_localization_state(request_gps_state = True)

    print(graph_nav_client.get_localization_state(request_gps_state = True))

    print()

    with open('test2_graphnav_state.txt', 'w') as file:
        file.write(state)

    with open('test2_graphnav_gps.txt', 'w') as file:
        file.write(gps)


