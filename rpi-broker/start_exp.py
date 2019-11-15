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

# original, limit_bw, lr, limit_bw_lr, temp_#
test = 'original'

# bw setting
if 'limit_bw' in test:
    bw = 100 # 100kbps=13kB/s
else:
    bw = 10000 # 10000kbps=13MB/s
# lr setting
if 'lr' in test:
    lr = 1
    input_size = 100000 # 100MB
else:
    lr = 0
    input_size = 0

def main():
    if len(sys.argv) == 2:
    #    pt_interval = float(sys.argv[1])
    #    input_size = int(sys.argv[2])
    #    output_size = int(sys.argv[3])
        exec_time = int(sys.argv[1])

    # preparation
    exp.clean_data_file()
    # time sync on all Pi's
    exp.set_date()
    # set rpi3's freq to 1200MHz
    exp_set.set_Pi3_freq(1200000)
    # bw settings
    exp_set.set_bw(bw)

    exp.start_bridge()
    print("Bridge is started. Please make sure:")
    print("(1) Pi Broker is started on 172.27.0.1.")
    print("(2) All ESPs are ready with ready msgs showing up on broker.")
    input("Press Enter to continue...")

    exp.start_esp(lr)
    exp.start_pi_zero(0.2, input_size, 20, exec_time)
    exp.start_pi_3(0.2, input_size, 80, exec_time)
    exp.start_data_collection(test)

    time.sleep(exec_time + 10)

    exp.kill_data_collection()
    exp.kill_bridge()

    # clean bw configurations
    exp_set.reset_bw()



if __name__ == '__main__':
    main()
