import ultrasonic, door, limit_switch
import flask_webserver

import multiprocessing

front_door = door.Door()
door_limit_switch = limit_switch.LimitSwitch(front_door.door_collision_isr())
door_ultrasonic = ultrasonic.Ultrasonic() # y axis detect



def door_collision_setup():
    limit_switch.lsw_setup(5)
    ultrasonic.ultrasonic_setup(26,6)


if __name__ == "__main__":
    door_collision_setup()


