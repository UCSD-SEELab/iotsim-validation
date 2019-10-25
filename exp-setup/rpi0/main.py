#!/usr/bin/python3

'''
Main script on Raspberry Pi Zero.
Take a picture and send to MQTT broker continuously.
To use the default resolution:
	python3 main.py
To set resolution in command line:
	python3 main.py 128 128

Author: Xiaofan Yu
Date: 10/23/2019
'''
from camera import myCamera
from mqtt_pub import myMQTTClient
import time
import sys

SERVER_IP = '192.168.137.34'
SERVER_PORT = 1884

def main():
	if len(sys.argv) > 1:
		res = (int(sys.argv[1]), int(sys.argv[2]))
		camera = myCamera(resolution=res)
	else:
		camera = myCamera()
	mqtt = myMQTTClient(server_ip=SERVER_IP, \
		server_port=SERVER_PORT)
	img_path = './image.jpg'
	
	while True:
	    camera.capture(sav_path=img_path)
	    mqtt.pub_img(img_path=img_path)


if __name__ == '__main__':
	main()
