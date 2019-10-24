#!/usr/bin/python3

'''
Main script on Raspberry Pi Zero.
Take a picture and send to MQTT broker continuously.

Author: Xiaofan Yu
Date: 10/23/2019
'''
from camera import myCamera
from mqtt_pub import myMQTTClient
import time

SERVER_IP = '192.168.137.210'
SERVER_PORT = 1884

def main():
	camera = myCamera()
	mqtt = myMQTTClient(server_ip=SERVER_IP, \
		server_port=SERVER_PORT)
	img_path = './image.jpg'
	
	while True:
		camera.capture(sav_path=img_path)
		mqtt.pub_img(img_path=img_path)


if __name__ == '__main__':
	main()
