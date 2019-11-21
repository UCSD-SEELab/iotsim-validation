#!/usr/bin/python3

'''
Run power measurements and trigger model fitting.

Author: Xiaofan Yu
Date: 11/20/2019
'''
import os
import time
from powermeter import PowerMeter
import subprocess
from fit_model import ModelFitting

PWR_FILE = './power.txt'
Pi_IP = '192.168.1.62'
MLP_LAYERS = [[14], [24, 16], [40, 32], [50, 32], [64, 32], [76, 32], \
        [92, 32], [104, 64], [118, 64], [132, 64]]
REG_MODEL = ['linear', 'poly', 'exp', 'log']

def pwr_callback(pwr):
    if pwr_callback.start_time is None:
        pwr_callback.start_time = time.time()

    pwr_callback.pwr_data.append(
            [float(time.time() - pwr_callback.start_time), pwr]
            )

pwr_callback.pwr_data = []
pwr_callback.start_time = None

def cal_avg_pwr(pwr_data):
    prev_time = None
    energy = 0.0
    for data in pwr_data:
        cur_time = data[0]
        pwr = data[1]
        if prev_time is not None:
            energy += (cur_time - prev_time) * pwr
        prev_time = cur_time
    total_time = prev_time # last time stamp
    return energy / total_time

def run_mlp(hidden_layer, times):
    '''
    hidden_layer: a list showing the # of units in each hidden layer
    '''
    hidden_layer = [str(i) for i in hidden_layer] # convert to string element
    cmd = 'python3 mlp.py -m infer -l {} -p ./output.jpg -t {}'.format( \
            ' '.join(hidden_layer), times)
    print('Run MLP of hidden layer {} for {} times with {}'.format(, \
            hidden_layer, times, cmd))
    stdout, stderr = subprocess.Popen("ssh pi@{host} \'{cmd}\'".format( \
            host=Pi_IP, cmd=cmd), shell=True, \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print('result: ', stdout, stderr)
    return stdout

def run_lr(in_kB, out_kB, times):
    '''
    input and output are in units of kB
    '''
    cmd = 'python3 lr.py -i {} -o {} -t {}'.format(in_kB, out_kB, times)
    print('Run LR of input {} kB and output {} kB for {} times with \
            {}'.format(in_kB, out_kB, times, cmd))
    stdout, stderr = subprocess.Popen("ssh pi@{host} \'{cmd}\'".format( \
            host=Pi_IP, cmd=cmd), shell=True, \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print('result: ', stdout, stderr)
    return stdout

def set_Pi3_freq(freq):
    # freq can either be 600000 or 1200000 for 600MHz and 1200MHz
    freq_script = '/home/pi/iotsim-validation/script/set_freq.sh'
    for Pi_IP in Pi_3:
        cmd = 'sudo bash {} {}'.format(freq_script, freq)
        print('set freq on Pi {} to {} by {}'.format(Pi_IP, freq, cmd))
        process = subprocess.Popen("ssh pi@{host} \'{cmd}\'".format( \
            host=Pi_IP, cmd=cmd), shell=True, \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def log(str):
    print(str)
    with open('./result.txt'. 'a+') as f:
       f.write(str)
       f.write('\n')

def main():
    '''
    Fire workload, measure avg. power and apply to 4 candidate regressions.
    '''
    # fix frequency to 1200MHz
    set_Pi3_freq(1200000)
    # for MLP
    times = 10
    mac, avgPower, execTime = [], [], []
    for l in MLP_LAYERS:
        pm = PowerMeter('./power_mlp_{}.txt'.format(l))
        pwr_callback.pwr_data = []
        pm.run(pwr_callback)
        this_time, this_mac = run_mlp(l, times)
        pm.stop()
        this_power = cal_avg_pwr(pwr_callback.pwr_data)
        mac.append(this_mac)
        execTime.append(this_time)
        avgPower.append(this_power)
        print(this_time, this_mac, this_power)

    log('mac: {}'.format(mac))
    log('mac: {}'.format(avgPower))
    log('mac: {}'.format(execTime))
    # try to fit
    ModelFit = ModelFitting()
    X = np.array(mac)
    Y1 = np.array(avgPower)
    Y2 = np.array(execTime)
    for model in REG_MODEL:
        # case can be power3b, time3b, power0, time0
        popt1, mse1 = ModelFit.fit(X, Y1, model, 'power3b')
        popt2, mse2 = ModelFit.fit(X, Y2, model, 'time3b')
        log('fit model {} for power'.format(model))
        log('popt: ', popt1)
        log('mse: ', mse1)
        log('fit model {} for time'.format(model))
        log('popt: ', popt2)
        log('mape: ', mse2)



if __name__ == '__main__':
    main()
