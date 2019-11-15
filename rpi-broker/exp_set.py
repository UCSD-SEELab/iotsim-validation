
#!/usr/bin/python3

'''
A script to set different experiment conditions

Author: Xiaofan Yu
Date: 11/13/2019
'''
import os

Pi_client = ['172.27.0.1', '172.27.0.2', '172.27.0.3', '172.27.0.4', '172.27.0.5', '172.27.0.6']

def set_bridge_freq(freq):
    # freq can either be 600000 or 1200000 for 600MHz and 1200MHz
    freq_script = '/home/pi/iotsim-validation/script/set_freq.sh'
    cmd = 'sudo bash {} {}'.format(freq_script, freq)
    print('set freq on Bridge Pi to {} by {}'.format(freq, cmd))
    process = subprocess.Popen("ssh {user}@{host} \'{cmd}\'".format( \
        user='pi', host=Bridge_IP, cmd=cmd), shell=True, \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def set_bw(bw):
	# set all bw for wlan0 on all Pi's
	# desired_bw is in kbps
	bw_script = '/home/pi/iotsim-validation/script/set_bw.sh'
	cmd = 'sudo bash {} {}'.format(freq_script, bw)
	for Pi_IP in Pi_client:
    	print('set bandwidth on pi {} to {}kbps by {}'.format(Pi_IP, bw, cmd))
    	process = subprocess.Popen("ssh {user}@{host} \'{cmd}\'".format( \
	        user='pi', host=Pi_IP, cmd=cmd), shell=True, \
	        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def reset_bw():
	# reset all bw for wlan0 on all Pi's
	bw_script = '/home/pi/iotsim-validation/script/reset_bw.sh'
	cmd = 'sudo bash {}'.format(freq_script)
	for Pi_IP in Pi_client:
    	print('set bandwidth on pi {} by {}'.format(Pi_IP, cmd))
    	process = subprocess.Popen("ssh {user}@{host} \'{cmd}\'".format( \
	        user='pi', host=Pi_IP, cmd=cmd), shell=True, \
	        stdout=subprocess.PIPE, stderr=subprocess.PIPE)