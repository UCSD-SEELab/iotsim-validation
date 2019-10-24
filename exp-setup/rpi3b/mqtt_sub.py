#!/usr/bin/python3

'''
Example module to receive picture from Raspberry Pi
Zero via MQTT.
Work on Python 3.5.3 of Raspberry Pi 3B+

Author: Xiaofan Yu
Date: 10/23/2019
'''
import paho.mqtt.client as mqtt
MQTT_SERVER = 'localhost'
MQTT_PORT = 1884

class myMQTTReceiver():
	def __init__(self, topic=None, server_ip=None, \
		server_port=None, client_id='rpi3b'):
		self.topic = topic
		self.hostname = server_ip
		self.port = server_port
		self.client_id = client_id
		self.client = mqtt.Client(client_id='rpi3b')
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.connect(host=self.hostname, port=self.port)


	# The callback for when the client receives a CONNACK response from the server.
	def on_connect(self, client, userdata, flags, rc):
	    print("Connected with result code "+str(rc))

	    # Subscribing in on_connect() means that if we lose the connection and
	    # reconnect then subscriptions will be renewed.
	    self.client.subscribe(self.topic)
	    # The callback for when a PUBLISH message is received from the server.


	def on_message(self, client, userdata, msg):
	    # more callbacks, etc
	    # Create a file with write byte permission
	    with open('./output.jpg', "wb") as f:
		    f.write(msg.payload)
		    print("Image Received")
		    f.close()


def main():
	# Blocking call that processes network traffic, dispatches callbacks and
	# handles reconnecting.
	# Other loop*() functions are available that give a threaded interface and a
	# manual interface.
	mqttRev = myMQTTReceiver(topic='rpi0/img', server_ip=MQTT_SERVER, \
		server_port=MQTT_PORT)
	mqttRev.client.loop_forever()

if __name__ == '__main__':
    main()
