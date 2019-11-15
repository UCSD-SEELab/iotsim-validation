#!/usr/bin/python3

'''
A plot script to visualize collected data.
Work on Python 3 on Linux.

To run, you need to specify a test case:
    python3 plot.py original

Author: Xiaofan Yu
Date: 11/14/2019
'''
import matplotlib.pyplot as plt
import os
import sys

def read_power(file_name):
    power = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = line.strip().split(',')
            power_data = float(data[1])
            power.append(power_data)
    return power

def read_temperature(file_name):
    # only Pi's data contains temperature data
    temp = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = line.strip().split(',')
            temp_data = float(data[2])
            temp.append(temp_data)
    return temp

def read_delay(file_name):
    delay = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = line.strip().split(',')
            if '172.27' in file_name:
                # Pi's data
                delay_data = float(data[3])
            else: # esp's data
                delay_data = float(data[2])
            delay.append(delay_data)
    return delay

all_devices = ['172.27.0.1', '172.27.0.2', '172.27.0.3', '172.27.0.4',
        '172.27.0.5', '172.27.0.6', 'esp1', 'esp2', 'esp3', 'esp4']
def main():
    if len(sys.argv) >= 2:
        test_case = sys.argv[1]
        data_dir = './' + test_case
    else:
        print('Please specify a test case!')
        exit(0)
    print('Test case: {}'.format(test_case))
    fig, ax = plt.subplots(nrows=5, ncols=2, figsize=(16,10))
    i, j = 0, 0 # position in subplots
    for device in all_devices:
        file_path = data_dir + '/' + device + '.txt'
        power = read_power(file_path)
        if '172.27' in device:
            temp = read_temperature(file_path)
        delay = read_delay(file_path)
        print('{}: avg power: {}, avg delay: {}'.format(device, \
            sum(power) / len(power),sum(delay) / len(delay)))

        # plot
        length = len(power)
        #length = 178
        x = range(length)

        color = 'tab:red'
        ax[i, j].plot(x, power[:length], color=color)
        ax[i, j].set_title('{}'.format(device))
        ax[i, j].set_xlabel('time step')
        ax[i, j].set_ylabel('power', color=color)
        ax[i, j].tick_params(axis='y', labelcolor=color)

        if '172.27' in device:
            ax2 = ax[i, j].twinx()
            color = 'tab:blue'
            ax2.plot(x, temp[:length], color=color)
            ax2.set_ylabel('temperature', color=color)
            ax2.tick_params(axis='y', labelcolor=color)

        # update i, j, move to the next plot
        if j == 0:
            j += 1
        else:
            j = 0
            i += 1
    fig.tight_layout()
    fig.suptitle('Power and Temperature Data in {} Test'.format(test_case))
    plt.show()

if __name__ == '__main__':
    main()

