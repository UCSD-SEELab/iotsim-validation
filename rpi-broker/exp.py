#!/usr/bin/python3

'''
A script containing all functions called in start_exp.py

Author: Xiaofan Yu
Date: 11/10/2019
'''
import paho.mqtt.publish as publish
import os
import subprocess

dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = dir_path + '/../log'
broker_log = log_dir + '/broker.log'
data_collect_log = log_dir + '/data.log'
data_collect_script = dir_path + '/data_collection.py'

Broker_IP = '172.27.0.1'
Broker_port = 61613
Bridge_IP = '172.27.0.5'
Bridge_config = '/home/pi/iotsim-validation/rpi-broker/mosquitto-eth0.conf'
Bridge_script = '/home/pi/iotsim-validation/rpi-mqtt/mqtt_bridge.py'
Pi_zero = ['172.27.0.2', '172.27.0.3', '172.27.0.4']
Pi_zero_script = '/home/pi/iotsim-validation/rpi-mqtt/mqtt_client.py'

def start_bridge():
	# start broker
	broker_log_path = '/home/pi/broker.log'
	cmd = 'mosquitto -c {} -p 61613 -v >> {} 2>&1 &'.format(\
		Bridge_config, broker_log_path)
	print('start broker on bridge by {}'.format(cmd))
	process = subprocess.Popen("ssh {user}@{host} {cmd}".format( \
		user='pi', host=Bridge_IP, cmd=cmd), shell=True, \
		stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	print('result: ', stdout, stderr)

	# start bridging script
	bridge_log_path = '/home/pi/bridge.log'
	cmd = 'python3 {} >> {} 2>&1 &'.format(bridge_script, \
		bridge_log_path)
	print('start bridging script on bridge by {}'.format(cmd))
	process = subprocess.Popen("ssh {user}@{host} {cmd}".format( \
		user='pi', host=Bridge_IP, cmd=cmd), shell=True, \
		stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	print('result: ', stdout, stderr)

def kill_bridge():
	# kill bridge script
	cmd = 'pgrep -f mqtt_bridge.py'
	print('get bridging script\'s PID on bridge by {}'.format(cmd))
	process = subprocess.Popen("ssh {user}@{host} {cmd}".format( \
		user='pi', host=Bridge_IP, cmd=cmd), shell=True, \
		stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	print('result: ', stdout, stderr)
	pid = int(stdout)

	cmd = 'sudo kill -9 {}'.format(pid)
	print('kill bridging script on bridge by {}'.format(cmd))
	process = subprocess.Popen("ssh {user}@{host} {cmd}".format( \
		user='pi', host=Bridge_IP, cmd=cmd), shell=True, \
		stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	print('result: ', stdout, stderr)

	# kill broker
	# kill bridge script
	cmd = 'pgrep -f mosquitto'
	print('get mosquitto broker\'s PID on bridge by {}'.format(cmd))
	process = subprocess.Popen("ssh {user}@{host} {cmd}".format( \
		user='pi', host=Bridge_IP, cmd=cmd), shell=True, \
		stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	print('result: ', stdout, stderr)
	pid = int(stdout)

	cmd = 'sudo kill -9 {}'.format(pid)
	print('kill mosquitto broker on bridge by {}'.format(cmd))
	process = subprocess.Popen("ssh {user}@{host} {cmd}".format( \
		user='pi', host=Bridge_IP, cmd=cmd), shell=True, \
		stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	print('result: ', stdout, stderr)

def start_esp():
	publish.single(topic='cmd', payload='start', \
		hostname=Broker_IP, port=Broker_port)

def start_pi_zero(pt_interval, fake_size, exec_time):
	for Pi_zero_IP in Pi_zero:
		log_path = '/home/pi/client.log'
		cmd = 'python3 {} {} {} {} {} >> {} 2>&1 &'.format(\
			Pi_zero_script, Pi_zero_IP, pt_interval, \
			fake_size, exec_time, log_path)
		print('start mqtt client on pi pi zero by {}'.format(cmd))
		process = subprocess.Popen("ssh {user}@{host} {cmd}".format( \
			user='pi', host=Pi_zero_IP, cmd=cmd), shell=True, \
			stdout=subprocess.PIPE,
	        stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()
		print('result: ', stdout, stderr)

def start_data_collection():
	cmd = 'python3 {} >> {} 2>&1 &'.format(data_collect_script, \
		data_collect_log)
	print('start data_collection by {}.'.format(cmd))
	os.popen(cmd)
	# print('result: {}'.format(stream.read()))

def kill_data_collection():
	# find pid of data collection script
	cmd = 'pgrep -f data_collection'
	stream = os.popen(cmd)
	pid = int(stream.read())
	# kill it
	cmd = 'sudo kill -9 {}'.format(pid)
	print('kill data_collection by {}.'.format(cmd))
	os.popen(cmd)
