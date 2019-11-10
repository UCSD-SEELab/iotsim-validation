#!/usr/bin/python3

'''
A bridge to connect ESP8266 mesh and RPi mesh.
	1) act as a MQTT server and receive all the message from ESP8266s.
	2) act as a MQTT client, forward esp's data to broker.
Work on Python 3.5.3 of Raspberry Pi Zero

To start the bridge, simply run the script.
	python3 mqtt_bridge.py

Author: Xiaofan Yu
Date: 11/8/2019
'''
import paho.mqtt.client as mqtt
import time
import os
import sys

client_pi = None
client_esp = None
'''
This section is for connecting to center pi broker.
Act as a MQTT client.
'''
# The callback for when the client receives a CONNACK response from the server.
def on_connect_pi(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("cmd") # subscribe cmd topic

def on_message_pi(client, userdata, msg):
	# simply forward all the incoming messages
	print("Received from pi broker:" + msg.topic + " " + str(msg.payload))
	global client_esp
	if (msg.topic == 'cmd'):
		broadcast_topic = "painlessMesh/to/broadcast"
		try:
			client_esp.publish(topic=broadcast_topic, payload=msg.payload)
		except Exception as e:
			print(e)

broker_IP = '172.27.0.1'
broker_port = 61613

client_pi = mqtt.Client("Bridge")
client_pi.connect(broker_IP, broker_port, 60)

'''
This section is for forwarding ESP8266's msg.
Act as a MQTT server.
'''
# The callback for when the client receives a CONNACK response from the server.
def on_connect_esp(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("cmd") # subscribe cmd topic

def on_message_esp(client, userdata, msg):
	# simply forward all the incoming messages
	print("Received from ESP mesh:" + msg.topic + " " + str(msg.payload))
	global client_pi
	# format the topic, add time stamp to payload (power data of ESPs)
	data_topic = 'data/' + msg.topic
	data_payload = str(time.time()) + ',' + msg.payload
	try:
		client_pi.publish(topic=data_topic, payload=payload)
	except Exception as e:
		print(e)

# connect to the broker of ESPs
server_IP = '192.168.1.46' # localhost
server_port = 61613
client_esp = mqtt.Client()
client_esp.connect(server_IP, server_port, 60)
client_esp.on_connect = on_connect_esp
client_esp.on_message = on_message_esp
client_esp.loop_forever() # nonblocking version