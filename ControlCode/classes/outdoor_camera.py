##############################################################################
#                                 Outdoor Camera
# open CV base camera
#
## Modified from: https://github.com/miguelgrinberg/flask-video-streaming/blob/master/LICENSE
# to work with project EPRI_SPOT by Joelle Bailey, Spring 2024
##############################################################################

import os
import cv2
from .base_camera import BaseCamera

class Camera_outdoor(BaseCamera):
    video_source = 2

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera_outdoor.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera_outdoor, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera_outdoor.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera_outdoor.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            #try:
            yield cv2.imencode('.jpg', img)[1].tobytes()
            
