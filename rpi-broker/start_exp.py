#!/usr/bin/python3

'''
A script to start all programs remotely, specifying
all necessary parameters.
Work on Python 3.5.3 of Raspberry Pi Zero

To start, with 0.2s interval of power & temperature
collection, 1000kB data as input to Linear Regression,
sending 1Kbytes fake data per second,
running experiment for 300s.
    python3 start_exp.py 0.2 1000 1 300

Author: Xiaofan Yu
Date: 11/10/2019
'''
import sys
import exp
import exp_set
import time

# original, limit_bw, lr, temp
test = 'original'

if test == 'limit_bw':
    bw = 100 # 100kbps
else:
    bw = 10000
if test == 'lr':
    input_size = 1000 # 1000kB
else:
    input_size = 0
output_size = 1 # 1kB

def main():
    if len(sys.argv) == 5:
        pt_interval = float(sys.argv[1])
        input_size = int(sys.argv[2])
        output_size = int(sys.argv[3])
        exec_time = int(sys.argv[4])

    # preparation
    exp.clean_data_file()
    # time sync on all Pi's
    exp.set_date()
    # set bridge rpi3's freq to 1200MHz
    exp_set.set_bridge_freq(1200000)
    # bw settings
    exp_set.set_bw(bw)

    exp.start_bridge()
    print("Bridge is started. Please make sure:")
    print("(1) Pi Broker is started on 172.27.0.1.")
    print("(2) All ESPs are ready with ready msgs showing up on broker.")
    input("Press Enter to continue...")

    exp.start_esp()
    exp.start_pi(pt_interval, input_size, output_size, exec_time)
    exp.start_data_collection()

    time.sleep(exec_time + 10)

    exp.kill_data_collection()
    exp.kill_bridge()

    # clean bw configurations
    exp_set.reset_bw()



if __name__ == '__main__':
    main()
