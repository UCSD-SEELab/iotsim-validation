#!/usr/bin/python3

'''
A bridge to connect ESP8266 mesh and RPi mesh.
	1) act as a MQTT server and receives all the message from ESP8266s.
	2) act as a MQTT client, forward esp's data to broker, publish
	power and temperature data to broker.
Work on Python 3.5.3 of Raspberry Pi Zero

To start the client, you need to specify the IP of the client
and the interval you want it to send power/temp. No fake data 
mode for the bridge node.
	python3 mqtt_client.py 172.27.0.10 0.2 1000

Author: Xiaofan Yu
Date: 11/8/2019
'''
from ina219_pi import ina219_pi
import paho.mqtt.client as mqtt
# import threading
import time
import os
import sys
ADDRESS_INA219 = 0x44

'''
This section is for connecting to center pi broker.
Act as a MQTT client.
'''
myIP = None
broker_IP = '172.27.0.1'
broker_port = 61613
client_local = None

'''
This section is for forwarding ESP8266's msg.
Act as a MQTT server.
'''
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#") # subscribe all topics

def on_message(client, userdata, msg):
	# simply forward all the incoming messages
	print("Received from ESP mesh:" + msg.topic + " " + str(msg.payload))
	global client_local
	client_local.publish(topic=msg.topic, payload=msg.payload)

server_IP = '192.168.1.46' # localhost
server_port = 61613
client_forward = mqtt.Client()
client_forward.connect(server_IP, server_port, 60)
client_forward.on_message = on_message
client_forward.loop_start() # nonblocking version

#def pub_fake_data(size):
#	'''
#	Publish certain bytes of fake date every second.
#	'''
#	fake_str = 'x' * size
#	client.publish(topic='fake', payload=fake_str)

def read_temp():
	stream = os.popen('vcgencmd measure_temp | egrep -o \'[0-9]*\\.[0-9]*\'')
	output = float(stream.read())
	return output

def main():
	module_ina219 = ina219_pi(address=ADDRESS_INA219)

	# parse input arguments
	if len(sys.argv) == 3:
		myIP = str(sys.argv[1])
		pt_interval = float(sys.argv[2])
		fake_size = None
	else:
		print('Incomplete command line arguments!')
		exit(0)

	global client_local
	client_local = mqtt.Client(myIP)
	client_local.connect(broker_IP, broker_port, 60)

	# get power data and temperature data
	while True:
		time_stamp = time.time()
		power = module_ina219.read_power()
		temp = read_temp()
		msg = '{},{},{}'.format(time_stamp, power, temp)
		topic = 'data/{}'.format(myIP)
		client_local.publish(topic=topic, payload=msg)
		time.sleep(pt_interval)


if __name__ == '__main__':
	main()