#!/usr/bin/python3

'''
Example module to send picture via MQTT.
Work on Python 3.5.3 of Raspberry Pi Zero

Author: Xiaofan Yu
Date: 10/23/2019
'''
import paho.mqtt.publish as publish

class myMQTTClient():
	def __init__(self, topic='rpi0/img', server_ip=None, \
		server_port=None, client_id='rpi0'):
		self.topic = topic
		self.payload = None
		self.qos = 0
		self.hostname = server_ip
		self.port = server_port
		self.client_id = client_id
		self.busy = False # note whether single publish is done

	def pub_img(self, img_path):
		self.busy = True
		# Read the image and publish it
		try:
			with open(img_path, "rb") as f:
				fileContent = f.read()
				self.payload = bytearray(fileContent)
				# single publish the image payload
				publish.single(topic=self.topic, \
					payload=self.payload, \
					qos=self.qos, \
					hostname=self.hostname, \
					port=self.port, \
					client_id=self.client_id)
		except Exception as e:
			print(e)

		self.busy = False
