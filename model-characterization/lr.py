#!/usr/bin/python3

'''
Run Linear Regression to process data on Photon
Work on Python 3.5.3 of Raspberry Pi 3B+
To test this module with 100MB input and 80kB output for 10 times:
    python3 lr.py -i 100000 -o 80 -t 10

Author: Xiaofan Yu
Date: 10/29/2019
'''
import numpy as np
import argparse
import time
import RPi.GPIO as GPIO
import socket

UDP_IP = "169.254.209.38"
UDP_PORT = 5005
ST_MSG = b'start'
FI_MSG = b'stop'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class LinearRegression():
    def __init__(self, in_size, out_size):
        self.in_size = in_size
        self.out_size = out_size

        self.GenerateRandomWeights(in_size, out_size)

    def GenerateRandomWeights(self, row, col):
        self.w = np.random.normal(size=(row, col))

    def run(self, list_in):
        array_in = np.array(list_in)
        array_in = np.reshape(array_in, (-1))
        array_out = np.dot(array_in, self.w)
        return list(array_out.reshape(-1))

    def MAC(self):
        '''
        Calculate the number of MAC operations.
        '''
        return self.in_size * self.out_size

if __name__ == '__main__':
    '''
    Run inference of certain input size for certain times.
    '''
    # parse the parameters
    parser = argparse.ArgumentParser(description='Run Linear Regression \
            with specified input size for certain times.')
    parser.add_argument('-i', '--input', type=int, dest='input', \
            help='Input data size in kB.')
    parser.add_argument('-o', '--output', type=int, dest='output', \
            help='Output data size in kB.')
    parser.add_argument('-t', '--times', type=int, dest='times', default=1, \
            help='Number of times to run inference.')

    args = parser.parse_args()

    # convert KByte to number of floats, << 3 then >> 2
    in_size = args.input << 1
    out_size = args.output << 1
    lr = LinearRegression(in_size, out_size)
    a = np.random.normal(size=(1, in_size))

    sock.sendto(ST_MSG, (UDP_IP, UDP_PORT))
    st_time = time.time()
    for i in range(args.times):
        lr.run(a)
    run_time = time.time() - st_time
    sock.sendto(FI_MSG, (UDP_IP, UDP_PORT))
    mac = lr.MAC()
    print(run_time, mac)
