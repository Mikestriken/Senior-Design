##############################################################################
#                     Indoor Camera Class Python Script
# This python script is a 3rd party script cloned from https://github.com/miguelgrinberg/flask-video-streaming/blob/master/LICENSE
# MIT License applies for this file
# 
# Minimal modification were made by the EPRI_SPOT team.
# 
# This script defines the logic needed to retrieve frames from the indoor camera.
# 
# The operation / main loop this script is tied to is found in
# /ControlCode/flask_webserver/flask_webserver.py
#
# Created by Joelle Bailey, Spring 2024
##############################################################################

import io
import time
from picamera2 import Picamera2, Preview
from .base_camera import BaseCamera

class Camera(BaseCamera):
    @staticmethod
    def frames():
        with Picamera2() as camera:
            camera.configure(camera.create_video_configuration(main={"size": (2300,1290)}))
            camera.start()

            # let camera warm up
            time.sleep(2) 

            stream = io.BytesIO()
            try:
                while True:
                    camera.capture_file(stream, format='jpeg')
                    stream.seek(0)
                    yield stream.read()

                    # reset stream for next frame
                    stream.seek(0)
                    stream.truncate()
            finally:
                camera.stop()