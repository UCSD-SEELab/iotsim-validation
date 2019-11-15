#!/usr/bin/python3

'''
A data collection script running on RPi broker.
Save all subscribed data into certain folders.
Work on Python 3.5.3 of Raspberry Pi Zero

To run, please specify a test case. The script will create a folder in `data`
to store traces if there is no such directory.
    python3 data_collection.py original

Author: Xiaofan Yu
Date: 11/10/2019
'''
import paho.mqtt.client as mqtt
import os
import sys
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("data/#") # subscribe to all data
    #client.subscribe("status") # ready status channel

def on_message(client, userdata, msg):
    # save data
    print("Received from pi broker:" + msg.topic + " " + str(msg.payload))
    topic = msg.topic.split('/')
    if topic[0] == "data":
        sourceID = topic[1]
        file_name = dir_path + '/' + sourceID + '.txt'
        pt_data = msg.payload.decode('utf-8')
        source_time = float(pt_data.split(',')[0])
        delay_time = time.time() - source_time

        pt_data += ',' + str(delay_time)
        print(pt_data)
        with open(file_name, 'a+') as f:
            f.write(pt_data + '\r\n')

def main():
    if len(sys.argv) >= 2:
        test_case = sys.argv[1]
    else:
        print('Please specify the test case!')
        exit(0)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path += '/../data/' + test_case
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    print("data directory is {}".format(dir_path))

    broker_IP = '172.27.0.1'
    broker_port = 61613

    client = mqtt.Client("data_collection")
    client.connect(broker_IP, broker_port, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever() # nonblocking version

if __name__ == '__main__':
    main()
