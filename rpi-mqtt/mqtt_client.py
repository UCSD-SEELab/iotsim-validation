#!/usr/bin/python3

'''
Example module to publish power, temperature and fake data via MQTT.
Work on Python 3.5.3 of Raspberry Pi Zero

To start the client, you need to specify the IP of the client
and the interval you want it to send power/temp. You also need to specify the
# of Kbytes to as input to Linear Regression, the # of Kbytes to send after LR
every second. The last argument is the execution
time.
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
broker_IP = '172.27.0.1'
broker_port = 61613
client = None

def pub_fake_data(input_size, output_size):
    '''
    Publish certain bytes of fake date every second.
    Note the unit for input_size and output_size are kB.
    '''
    x = threading.currentThread()
    print('start lr with input {}kB and output {}kB'.format(input_size, output_size))
    # covert input_size and output_size from KB to B
    input_size = input_size << 10
    output_size = output_size << 10
    if input_size > 0:
        # divide by 4, obtain the # of floats we need
        mylr = lr.LinearRegression(input_size >> 2, output_size >> 2)
        a = np.random.normal(size=(1, input_size >> 2))

    fake_str = 'x' * output_size
    last_time = time.time()
    while getattr(x, "do_run", True):
        if input_size > 0:
            st_lr = time.time()
            mylr.run(a)
            fi_lr = time.time()
            print('Run {}'.format(fi_lr - st_lr))
        client.publish(topic='fake', payload=fake_str)
        print('Send {}'.format(time.time() - fi_lr))
        try:
            print(last_time + 1.0 - time.time())
            time.sleep(last_time + 1.0 - time.time())
        except Exception as e: # time overflow
            print(e)
        last_time = time.time()

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
        output_size = int(sys.argv[4])
        exec_time = int(sys.argv[5])
    else:
        print('Incomplete command line arguments!')
        exit(0)

    global client
    client = mqtt.Client(myIP)
    client.connect(broker_IP, broker_port, 60)

    if output_size > 0:
        x = threading.Thread(target=pub_fake_data, \
            args=(input_size, output_size))
        x.start()

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

    # collect the thread
    if output_size > 0:
        x.do_run = False
        x.join()
    print("End of experiment! :)")

if __name__ == '__main__':
    main()
