#!/usr/bin/python3

'''
Example module to publish power, temperature and fake data via MQTT.
Special scripts for RPi3_1. Subscribe data from broker, every time it receives
data from broker, it will process half of them and directly forward the rest 
half.
Work on Python 3.5.3 of Raspberry Pi Zero

To start the client, you need to specify the IP of the client
and the interval you want it to send power/temp. You also need to specify the
# of Kbytes to as input to Linear Regression, the # of Kbytes to send after LR
every second. The last argument is the execution time.
    python3 mqtt_client.py 172.27.0.2 0.2 1000 1 300

Author: Xiaofan Yu
Date: 11/8/2019
'''
from ina219_pi import ina219_pi
import paho.mqtt.client as mqtt
import threading
import time
import os
import sys
import lr
import numpy as np
ADDRESS_INA219 = 0x40 # no drop

myIP = None
broker_IP = '172.27.0.2'
broker_port = 61613
client = None
output_size = None

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("fake_rpi0") # subscribe to fake data
    #client.subscribe("status") # ready status channel

def on_message(client, userdata, msg):
    # save data
    print("Received from pi broker:" + msg.topic + " " + str(msg.payload))
    if msg.topic == "fake_rpi0":
        payload = msg.payload.decode('utf-8')
        data_size = len(payload)
        # get the input size and output size in Bytes
        input_size = data_size # input_size in Byte is half
        output_size = output_size << 10 # kB to B, output_size in Byte
        print('start lr with input {}B and output {}B'.format(input_size, output_size))

        mylr = lr.LinearRegression(input_size >> 2, output_size >> 2)
        a = np.random.normal(size=(1, input_size >> 2))
        st_lr = time.time()
        mylr.run(a)
        fi_lr = time.time()
        print('Run {}'.format(fi_lr - st_lr))
        # the total size of published data is input_size + output_size
        #client.publish(topic="fake_rpi0", payload=payload[:(input_size+output_size)])
        #print('Send {}'.format(time.time() - fi_lr))

def read_temp():
    stream = os.popen('vcgencmd measure_temp | egrep -o \'[0-9]*\\.[0-9]*\'')
    output = float(stream.read())
    return output

def main():
    module_ina219 = ina219_pi(address=ADDRESS_INA219)

    # parse input arguments
    if len(sys.argv) == 6:
        myIP = str(sys.argv[1])
        pt_interval = float(sys.argv[2])
        input_size = int(sys.argv[3])
        global output_size
        output_size = int(sys.argv[4])
        exec_time = int(sys.argv[5])
    else:
        print('Incomplete command line arguments!')
        exit(0)

    global client
    client = mqtt.Client(myIP)
    client.connect(broker_IP, broker_port, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start() # nonblocking version

    # get power data and temperature data
    start_time = time.time()
    while True:
        time_stamp = time.time()
        power = module_ina219.read_power()
        temp = read_temp()
        msg = '{},{},{}'.format(time_stamp, power, temp)
        topic = 'data/{}'.format(myIP)
        client.publish(topic=topic, payload=msg)
        time.sleep(pt_interval)

        if time.time() - start_time >= exec_time:
            break

    print("End of experiment! :)")

if __name__ == '__main__':
    main()
