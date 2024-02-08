import ultrasonic, door_operation, limit_switch
import flask_webserver

import multiprocessing

def door_collision_setup():
    limit_switch.lsw_setup(5)
    ultrasonic.ultrasonic_setup(26,6)


if __name__ == "__main__":
    door_collision_setup()


