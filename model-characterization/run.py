#!/usr/bin/python3

'''
Run power measurements and trigger model fitting.
To run, please specify the worload and device type:
    python3 run.py 3b_mlp # rpi3b running mlp
    or
    python3 run.py 0_lr # rpi0 running lr

Author: Xiaofan Yu
Date: 11/20/2019
'''
import os
import sys
import time
from powermeter import PowerMeter
import subprocess
from fit_model import ModelFitting
import numpy as np

PWR_FILE = './power.txt'
Pi_IP = '169.254.84.164'
MLP_LAYERS = [[6], [12], [18], [24, 8], [31, 16], [37, 16], [43, 16], \
        [49, 16], [55, 32], [64, 32]]
REG_MODEL = ['linear', 'poly', 'exp', 'log']
times_mlp = 500
times_lr = 500
input_size_lr = 100000 # 100MB

def pwr_callback(pwr):
    if pwr_callback.start_time is None:
        pwr_callback.start_time = time.time()

    pwr_callback.pwr_data.append(
            [float(time.time() - pwr_callback.start_time), pwr]
            )

pwr_callback.pwr_data = []
pwr_callback.start_time = None

def cal_avg_pwr(pwr_data):
    start_time, prev_time = None, None
    last_pwr = None
    energy = 0.0
    for data in pwr_data:
        cur_time = data[0]
        pwr = data[1]
        # print(cur_time, pwr)
        if start_time is None:
            start_time = cur_time # first time stamp
        if prev_time is not None:
            if pwr < 10.0: # check
                energy += (cur_time - prev_time) * pwr
                last_pwr = pwr
            elif last_pwr is not None:
                energy += (cur_time - prev_time) * last_pwr
        prev_time = cur_time
    total_time = prev_time - start_time # last time stamp
    log("Total energy: {}. Total time: {}".format(energy, total_time))
    return energy / total_time

def run_mlp(hidden_layer, times):
    '''
    hidden_layer: a list showing the # of units in each hidden layer
    '''
    hidden_layer = [str(i) for i in hidden_layer] # convert to string element
    cmd_pi = 'python3 /home/pi/iotsim-validation/model-characterization/mlp.py \
            -m infer -l {} -t {}'.format(' '.join(hidden_layer), times)
    cmd = "ssh pi@{host} {cmd}".format(host=Pi_IP, cmd=cmd_pi) 
    print('Run MLP of hidden layer {} for {} times with {}'.format( \
            hidden_layer, times, cmd))
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    res = proc.stdout.read().decode('utf-8').strip().split()
    res = [float(r) for r in res]
    print('result: ', res)
    return res

def run_lr(in_kB, out_kB, times):
    '''
    input and output are in units of kB
    '''
    cmd_pi = 'python3 /home/pi/iotsim-validation/model-characterization/lr.py \
            -i {} -o {} -t {}'.format(in_kB, out_kB, times)
    cmd = 'ssh pi@{host} {cmd}'.format(host=Pi_IP, cmd=cmd_pi)
    print('Run LR of input {} kB and output {} kB for {} times with \
            {}'.format(in_kB, out_kB, times, cmd))
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    res = proc.stdout.read().decode('utf-8').strip().split()
    res = [float(r) for r in res]
    print('result: ', res)
    return res

def set_Pi3_freq(freq):
    # freq can either be 600000 or 1200000 for 600MHz and 1200MHz
    freq_script = '/home/pi/iotsim-validation/script/set_freq.sh'
    cmd = 'sudo bash {} {}'.format(freq_script, freq)
    print('set freq on Pi {} to {} by {}'.format(Pi_IP, freq, cmd))
    process = subprocess.Popen("ssh pi@{host} \'{cmd}\'".format( \
        host=Pi_IP, cmd=cmd), shell=True, \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def log(str):
    print(str)
    with open('./result.txt', 'a+') as f:
       f.write(str)
       f.write('\n')

def main():
    '''
    Fire workload, measure avg. power and apply to 4 candidate regressions.
    '''
    # determine run mlp or lr
    if len(sys.argv) == 2:
        mode = sys.argv[1]
    else:
        print('Please specify the workload to run, mlp or lr!')
        exit(0)
    
    # fix frequency to 1200MHz
    set_Pi3_freq(1200000)
    # for MLP
    mac, avgPower, execTime = [], [], []
    if 'mlp' in mode:
        for l in MLP_LAYERS:
            pm = PowerMeter('./pwr/power{}_{}.txt'.format(mode, l))
            pwr_callback.pwr_data = []
            pm.run(pwr_callback)
            this_time, this_mac = run_mlp(l, times_mlp)
            pm.stop()
            this_time = this_time / times_mlp # divide by times
            this_power = cal_avg_pwr(pwr_callback.pwr_data)
            mac.append(this_mac)
            execTime.append(this_time)
            avgPower.append(this_power)
            print(this_time, this_mac, this_power)
    elif 'lr' in mode:
        for output_size in range(25, 251, 25):
            pm = PowerMeter('./pwr/power{}_{}_{}.txt'.format(mode, \
                    input_size_lr, output_size))
            pwr_callback.pwr_data = []
            pm.run(pwr_callback)
            # input is 100MB, output is output_size kB
            this_time, this_mac = run_lr(input_size_lr, output_size, times_lr)
            pm.stop()
            this_time = this_time / times_lr # divide by times
            this_power = cal_avg_pwr(pwr_callback.pwr_data)
            mac.append(this_mac)
            execTime.append(this_time)
            avgPower.append(this_power)
            print(this_time, this_mac, this_power)
    else:
        print('Unsupported mode!')
        exit(0)

    log('mac: {}'.format(mac))
    log('avgPower: {}'.format(avgPower))
    log('execTime: {}'.format(execTime))
    # try to fit
    ModelFit = ModelFitting()
    X = np.array(mac)
    Y1 = np.array(avgPower)
    Y2 = np.array(execTime)
    for model in REG_MODEL:
        # case can be power3b_{mlp/lr}, time3b_{mlp/lr}, power0_{mlp/lr}, 
        # time0_{mlp/lr}
        popt1, mse1 = ModelFit.fit(X, Y1, model, 'power'+mode)
        popt2, mse2 = ModelFit.fit(X, Y2, model, 'time'+mode)
        log('fit model {} for power{}'.format(model, mode))
        log('popt: {}'.format(popt1))
        log('mse: {}'.format(mse1))
        log('fit model {} for time{}'.format(model, mode))
        log('popt: {}'.format(popt2))
        log('mape: {}'.format(mse2))



if __name__ == '__main__':
    main()
