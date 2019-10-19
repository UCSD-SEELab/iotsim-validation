#!/usr/bin/python3

'''
Example module to capture picture with pycamera.
Work on Python 3.7.3.

Author: Xiaofan Yu
Date: 10/18/2019
'''
from picamera import PiCamera
import time

class myCamera():
    def __init__(self, res, path):
        # init object and settings
        self.camera = PiCamera()
        self.camera.resolution = res
        self.sav_path = path

        # start preview
        self.camera.start_preview()

    def __del__(self):
        self.camera.stop_preview()

    def capture(self):
        self.camera.capture(self.sav_path)


if __name__ == '__main__':
    myCamera = myCamera((1000, 800), '/home/pi/Desktop/image.jpg')
    myCamera.capture()

