#!/bin/bash
# Configure mesh network.
# Need to run install.sh before running this script
# To use, specify the desired IP in command line:
# 	sudo bash ./batsetup-rpi.sh 172.27.0.1/16
#
# Author: Xiaofan Yu
# Date: 11/6/2019

# Check whether command line argument is given
if [ "$1" = "" ]; then
	echo "Parameter IP is empty!"
	exit
fi
CHANNEL=3;
ESSID=my-mesh;
IP=$1;

# Disable wpa_supplicant
killall wpa_supplicant;

# set interfaces
ip link set wlan0 down;
iw wlan0 set type ibss;
iwconfig wlan0 mode ad-hoc;
iwconfig wlan0 channel $CHANNEL;
ip link set wlan0 up;
iw wlan0 ibss join my-mesh 2432;
modprobe batman-adv;
batctl if add wlan0;
ip link set up dev wlan0;
ip link set up dev bat0;
ifconfig bat0 $IP;

# show results
iwconfig; ifconfig;
