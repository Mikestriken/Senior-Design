# import statemachine



from .modules import ultrasonic, door, limit_switch
from .webserver import flask_webserver

front_door = door.Door()
door_limit_switch = limit_switch.LimitSwitch(front_door.door_collision_isr())
door_ultrasonic = ultrasonic.Ultrasonic() # y axis detect


# GPIO.setwarnings(False)



if __name__ == "__main__":
    while(1):
        a = 1


