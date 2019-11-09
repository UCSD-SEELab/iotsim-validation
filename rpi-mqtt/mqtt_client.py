#!/usr/bin/python3

'''
Example module to publish power, temperature and fake data via MQTT.
Work on Python 3.5.3 of Raspberry Pi Zero

To start the client, you need to specify the IP of the client
and the interval you want it to send power/temp. If you want it
to send fake data at the same time, you need to specify the 
# of bytes to send every second:
	python3 mqtt_client.py 172.27.0.2 0.2 1000

Author: Xiaofan Yu
Date: 11/8/2019
'''
from ina219-pi import ina219_pi
import paho.mqtt.client as mqtt
import threading
import time
import os

ADDRESS_INA219 = 0x44

myIP = None
broker_IP = '192.168.1.46'
broker_port = 61613
client = None

def pub_fake_data(size):
	'''
	Publish certain bytes of fake date every second.
	'''
	fake_str = 'x' * size
	client.publish(topic='fake', payload=fake_str)

def read_temp():
	stream = os.popen('vcgencmd measure_temp | egrep -o \'[0-9]*\\.[0-9]*\'')
	output = float(stream.read())
	return output

def main():
	module_ina219 = ina219_pi(address=ADDRESS_INA219)

	# parse input arguments
	if len(sys.argv) == 4:
		myIP = str(sys.argv[1])
		pt_interval = float(sys.argv[2])
		fake_size = int(sys.argv[3])
	elif len(sys.argv) == 3:
		myIP = str(sys.argv[1])
		pt_interval = float(sys.argv[2])
		fake_size = None
	else:
		print('Incomplete command line arguments!')
		exit(0)

	global client
	client = mqtt.Client(myIP)
	client.connect(broker_IP, broker_port, 60)

	if (fake_size is not None):
		x = threading.Thread(target=pub_fake_data, args=(fake_size,))
    	x.start()

	# get power data and temperature data
	while True:
		time_stamp = time.time()
		power = module_ina219.read_power()
		temp = read_temp()
		msg = '{},{},{}'.format(time_stamp, power, temp)
		topic = 'data/{}'.format(myIP)
		client.publish(topic=topic., payload=msg)
		time.sleep(pt_interval)


if __name__ == '__main__':
	main()