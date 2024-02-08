import time, libcamera
from picamera2 import Picamera2, Preview

def camera_setup():
    global picam
    picam = Picamera2(camera_num=0)

    config = picam.create_preview_configuration(main={"size": (600, 500)})
    config["transform"] = libcamera.Transform(hflip=1, vflip=1)
    picam.configure(config)



def take_still():
    picam.start_preview()
    picam.start()
    
    time.sleep(2)

    #picam.capture_file("static/website_still.jpg")
    #picam.close()
    return picam.capture_image("main")

def close_cam():
    picam.close()


camera_setup()
take_still()
close_cam()
