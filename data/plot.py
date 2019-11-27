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
import numpy as np
import math
data_dir = None
result_file = './result.txt'

def read_file(file_name):
    dict = {} # define hash function
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = line.strip().split(',')
            time = float(data[0])
            power = float(data[1])
            if '172.27' in file_name:
                temp = float(data[2])
                delay = float(data[3])
                dict[time] = [power, temp, delay]
            else:
                delay = float(data[2])
                dict[time] = [power, delay]
    # sort by time
    time, power, temp, delay = [], [], [], []
    for t in sorted(dict):
        time.append(t)
        power.append(dict[t][0])
        if '172.27' in file_name:
            temp.append(dict[t][1])
            delay.append(dict[t][2])
        else:
            delay.append(dict[t][1])
    return time, power, temp, delay


# Align samples for the target timestamps
# target_ts, ts, vs should all be np array
def align_samples(target_ts, ts, vs):
    assert len(ts) == len(vs)
    ret_list = []

    # List of interval
    vs_in_interval = []
    target_idx = 0
    target_t = target_ts[0]
    def commit_interval(ret_list, vs_in_interval, target_idx):
        if vs_in_interval:
            ret_list.append(np.array(vs_in_interval).mean())
        else:
            ret_list.append(np.nan)

        # update target_idx and target_t to next stamp in target_ts
        target_idx += 1
        if target_idx < len(target_ts):
            return [], target_ts[target_idx], target_idx

        return [], None, target_idx

    prev_t = None
    prev_v = None
    for cur_t, cur_v in zip(ts, vs):
        while target_t is not None and target_t < cur_t:
            if prev_t and prev_t < target_t:
                # fill the samples in the interval
                vs_in_interval.append(prev_v + (cur_v - prev_v) * \
                        (target_t - prev_t) / (cur_t - prev_t))
            vs_in_interval, target_t, target_idx = \
                    commit_interval(ret_list, vs_in_interval, target_idx)

        # Prepare the next target
        vs_in_interval.append(cur_v)
        prev_t = cur_t
        prev_v = cur_v

    if target_t is not None: # last available timestamp
        vs_in_interval, target_t, target_idx = \
                commit_interval(ret_list, vs_in_interval, target_idx)

    # fill nan for unavailable target rates
    while target_idx < len(target_ts):
        ret_list.append(np.nan)
        target_idx += 1

    assert(len(ret_list) == len(target_ts))
    return ret_list

def read_powermeter():
    # read the power of 172.270.0.1 from powermeter
    power_file = data_dir + '/power_broker.txt'
    time, power = [], []
    with open(power_file, 'r') as f:
        line = f.readline() # skip first line
        lines = f.readlines()
        for line in lines:
            data = line.strip().split(',')
            time.append(float(data[0])/1000.0) # ms->s
            power.append(float(data[-1])) # W
    return time, power

def log(str):
    print(str)
    with open(result_file, 'a+') as f:
        f.write(str)

all_devices = ['172.27.0.1', '172.27.0.2', '172.27.0.3', '172.27.0.4',
        '172.27.0.5', '172.27.0.6']#, 'esp1', 'esp2', 'esp3', 'esp4']
def main():
    if len(sys.argv) >= 2:
        test_case = sys.argv[1]
        global data_dir
        data_dir = './' + test_case
    else:
        print('Please specify a test case!')
        exit(0)
    log('Test case: {}\n'.format(test_case))
    fig, ax = plt.subplots(nrows=5, ncols=2, figsize=(16,10))
    i, j = 0, 0 # position in subplots
    for device in all_devices:
        file_path = data_dir + '/' + device + '.txt'
        time, power, temp, delay = read_file(file_path)
        if 'old' not in test_case and device == '172.27.0.1':
            # use power in power_broker.txt if it is the central Pi
            time_pm, power_pm = read_powermeter()
            target_ts = np.array(time)
            time_pm = np.array(time_pm)
            power_pm = np.array(power_pm)
            power = align_samples(target_ts, time_pm, power_pm)
            # print(power)
            nan_cnt = 0
            try:
                while True:
                    idx = power.index(np.nan)
                    power.pop(idx)
                    time.pop(idx)
                    temp.pop(idx)
                    print(nan_cnt)
                    nan_cnt += 1
            except:
                print('no more nans!')
                pass
        time = [t - time[0] for t in time]
        log('{}: avg power: {}, max power: {}, min power: {}, \
            avg delay: {}\n'.format(device, sum(power) / len(power),
                max(power), min(power), sum(delay) / len(delay)))
        log('avg temp: {}, max temp: {}, min temp:{}'.format( \
                sum(temp) / len(temp), max(temp), min(temp)))

        # plot
        color = 'tab:red'
        ax[i, j].plot(time, power, color=color)
        ax[i, j].set_title('{}'.format(device))
        ax[i, j].set_xlabel('time step')
        ax[i, j].set_ylabel('power', color=color)
        ax[i, j].tick_params(axis='y', labelcolor=color)

        if '172.27' in device:
            ax2 = ax[i, j].twinx()
            color = 'tab:blue'
            ax2.plot(time, temp, color=color)
            ax2.set_ylabel('temperature', color=color)
            ax2.tick_params(axis='y', labelcolor=color)

        # update i, j, move to the next plot
        if j == 0:
            j += 1
        else:
            j = 0
            i += 1
    log('\r\n')
    fig.tight_layout()
    fig.suptitle('Power and Temperature Data in {} Test'.format(test_case))
    figname = './img/' + test_case + '.png'
    plt.savefig(figname, dpi=300)
    #plt.show()

if __name__ == '__main__':
    main()

