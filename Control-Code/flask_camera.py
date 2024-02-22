
import os
import cv2
from base_camera import BaseCamera

class Camera_outdoor(BaseCamera):
    video_source = 0

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

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

# def take_outdoor_picture():
#     # Open the default camera (usually the webcam)
#     cap = cv2.VideoCapture(0)

#     # Check if the camera opened successfully
#     if not cap.isOpened():
#         print("Error: Could not open camera.")
#         return

#     # Capture a frame
#     success, frame = cap.read()
#     ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
#     frame = buffer.tobytes()

#     # Check if the frame was captured successfully
#     if not ret:
#         print("Error: Failed to capture image.")
#         return

#     # Save the captured frame as an image file
#     # cv2.imwrite('captured_image.jpg', frame)

#     # Release the camera
#     cap.release()

#     # print("Image captured successfully.")
#     return frame
