#!/usr/bin/python3

'''
Example module to capture picture with pycamera.
Work on Python 3.5.3

Author: Xiaofan Yu
Date: 10/18/2019
'''
from picamera import PiCamera

class myCamera():
    def __init__(self, resolution=(1024, 1024)):
        # init object and settings
        self.camera = PiCamera()
        self.camera.resolution = resolution

        # start preview
        self.camera.start_preview()

    def __del__(self):
        self.camera.stop_preview()

    def capture(self, sav_path='./image.jpg'):
        self.camera.capture(sav_path)


if __name__ == '__main__':
    myCamera = myCamera((1000, 800))
    myCamera.capture('./image.jpg')

