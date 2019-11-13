#!/usr/bin/python3

'''
A script to start all programs remotely, specifying
all necessary parameters.
Work on Python 3.5.3 of Raspberry Pi Zero

To start, with 0.2s interval of power & temperature 
collection, sending 1000 bytes fake data per second,
running experiment for 300s.
    python3 start_exp.py 0.2 1000 300

Author: Xiaofan Yu
Date: 11/10/2019
'''
import sys
import exp
import time
def main():
    if len(sys.argv) == 4:
        pt_interval = float(sys.argv[1])
        fake_size = int(sys.argv[2])
        exec_time = int(sys.argv[3])

    # preparation
    exp.clean_data_file()
    
    # configurations
    # set rpi3's freq to 1200MHz

    
    #exp.start_bridge()
    print("Bridge is started. Please make sure:")
    print("(1) Pi Broker is started on 172.27.0.1.")
    print("(2) All ESPs are ready with ready msgs showing up on broker.")
    input("Press Enter to continue...")

    exp.start_esp()
    exp.start_pi(pt_interval, fake_size, exec_time)
    exp.start_data_collection()

    time.sleep(exec_time + 10)

    exp.kill_data_collection()
    exp.kill_bridge()



if __name__ == '__main__':
    main()
