#!/usr/bin/python3

'''
Main script on Raspberry Pi Zero

Author: Xiaofan Yu
Date: 10/23/2019
'''
from .camera import myCamera
from .mqtt_pub import myMQTTClient

def main():
	myCamera = myCamera()
	mqtt = myMQTTClient(server_ip=, server_port=1883)

	img_path = './image.jpg'
	myCamera.capture(sav_path=img_path)
	mqtt.pub_img(img_path=img_path)


if __name__ == '__main__':
	main()