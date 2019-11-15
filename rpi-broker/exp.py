#!/usr/bin/python3

'''
A script containing all functions to start experiments

Author: Xiaofan Yu
Date: 11/10/2019
'''
import paho.mqtt.publish as publish
import os
import subprocess
import time

broker_log = 'broker.log'
bridge_log = 'bridge.log'
data_collect_log = 'data.log'
pi_client_log = 'client.log'
data_collect_script = '/home/pi/iotsim-validation/rpi-broker/data_collection.py'
data_path = '/home/pi/iotsim-validation/data/' 
Bridge_script = '/home/pi/iotsim-validation/rpi-mqtt/mqtt_bridge.py'
Bridge_config = '/home/pi/iotsim-validation/rpi-broker/mosquitto-eth0.conf'
Pi_zero_script = '/home/pi/iotsim-validation/rpi-mqtt/mqtt_client.py'
freq_script = '/home/pi/iotsim-validation/script/set_freq.sh'

Broker_IP = '172.27.0.1'
Broker_port = 61613
Bridge_IP = '172.27.0.6'
Pi_client = ['172.27.0.1', '172.27.0.2', '172.27.0.3', '172.27.0.4', '172.27.0.5', '172.27.0.6']

def clean_data_file():
    # Note: we only want to clean the files in data directory.
    # We never want to clean them recursively!
    for item in os.listdir(data_path):
        if item.endswith('.txt'):
            os.remove(data_path + '/' + item)

def set_date():
    # time sync
    cmd = 'sudo date 0413144913'
    for Pi_IP in Pi_client:
        print('set time on Pi {} by {}'.format(Pi_IP, cmd))
        process = subprocess.Popen("ssh {user}@{host} \'{cmd}\'".format( \
            user='pi', host=Pi_IP, cmd=cmd), shell=True, \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def start_bridge():
    # start broker
    cmd = '/usr/local/sbin/mosquitto -c {} -p 61613 -v > {} 2>&1'.format(\
        Bridge_config, broker_log)
    print('start broker on bridge by {}'.format(cmd))
    process = subprocess.Popen("ssh {user}@{host} \'{cmd}\'".format( \
        user='pi', host=Bridge_IP, cmd=cmd), shell=True, \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # start bridging script
    cmd = 'python3 {} > {} 2>&1'.format(Bridge_script, bridge_log)
    print('start bridging script on bridge by {}'.format(cmd))
    process = subprocess.Popen("ssh {user}@{host} \'{cmd}\'".format( \
        user='pi', host=Bridge_IP, cmd=cmd), shell=True, \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def kill_bridge():
    # kill bridge script
    cmd = 'pkill -f mqtt_bridge.py'
    print('kill bridging script on bridge by {}'.format(cmd))
    stdout, stderr = subprocess.Popen("ssh {user}@{host} \'{cmd}\'".format( \
        user='pi', host=Bridge_IP, cmd=cmd), shell=True, \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print('result: ', stdout, stderr)

    # kill broker
    # kill bridge script
    cmd = 'pkill -f mosquitto'
    print('kill mosquitto broker on bridge by {}'.format(cmd))
    stdout, stderr = subprocess.Popen("ssh {user}@{host} \'{cmd}\'".format( \
        user='pi', host=Bridge_IP, cmd=cmd), shell=True, \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print('result: ', stdout, stderr)

def start_esp():
    print('start esp')
    publish.single(topic='cmd', payload='start', client_id='startesp', \
        hostname=Broker_IP, port=Broker_port)

def start_pi(pt_interval, input_size, output_size, exec_time):
    for Pi_IP in Pi_client:
        cmd = 'python3 {} {} {} {} {} {} > {} 2>&1'.format(\
            Pi_zero_script, Pi_IP, pt_interval, \
            input_size, output_size, exec_time, pi_client_log)
        print('start mqtt client on pi {} by {}'.format(Pi_IP, cmd))
        process = subprocess.Popen("ssh {user}@{host} \'{cmd}\'".format( \
            user='pi', host=Pi_IP, cmd=cmd), shell=True, \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def start_data_collection():
    cmd = 'python3 {} > {} 2>&1'.format(data_collect_script, \
        data_collect_log)
    print('start data_collection by {}.'.format(cmd))
    process = subprocess.Popen(cmd, shell=True)

def kill_data_collection():
    # find pid of data collection script
    cmd = "pkill -f data_collection"
    print("kill data_collection script with {}".format(cmd))
    stdout, stderr = subprocess.Popen(cmd, shell=True, \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print('result: ', stdout, stderr)
