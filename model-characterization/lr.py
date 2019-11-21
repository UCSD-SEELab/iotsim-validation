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
    parser = argparse.ArguimentParse(description='Run Linear Regression \
            with specified input size for certain times.')
    parser.add_argument('-i', '--input', type=int, dest='input', \
            help='Input data size in kB.')
    parser.add_argument('-o', '--output', type=int, dest='output', \
            help='Output data size in kB.')
    parser.add_argument('-t', '--times', type=int, dest='times', default=1, \
            help='Number of times to run inference.')

    args = parser.parse_args()

    # convert Byte to number of floats
    in_size = args.input >> 3
    out_size = args.output >> 3
    lr = LinearRegression(in_size, out_size)
    a = np.random.normal(size=(out_size, in_size))

    st_time = time.time()
    for i in range(args.times):
        lr.run(a)
    run_time = time.time() - st_time
    mac = lr.MAC()
    print(run_time, mac)

