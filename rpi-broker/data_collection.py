#!/usr/bin/python3

'''
A data collection script running on RPi broker.
Save all subscribed data into certain folders.
Work on Python 3.5.3 of Raspberry Pi Zero

To start:
	python3 data_collection.py

Author: Xiaofan Yu
Date: 11/10/2019
'''
import paho.mqtt.client as mqtt
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path += '/../data'
print("data directory is {}".format(dir_path))


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("data/#") # subscribe to all data

def on_message(client, userdata, msg):
	# save data
	print("Received from pi broker:" + msg.topic + " " + str(msg.payload))
	sourceID = msg.topic.split('/')[1]
	file_name = dir_path + '/' + sourceID + '.txt'

	with open(file_name, 'a+') as f:
		f.write(msg.payload + '\r\n')


broker_IP = '172.27.0.1'
broker_port = 61613

client = mqtt.Client("data_collection")
client.connect(broker_IP, broker_port, 60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever() # nonblocking version