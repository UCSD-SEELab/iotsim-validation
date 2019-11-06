#!/bin/sh -e
# Configure the mesh network.
# Need to run install.sh before running this script.
#
# Author: Xiaofan Yu
# Date: 11/5/2019

ESSID=my-mesh
# PWD=goodluck
CHANNEL=3
IP_ADDRESS=$1

# Disable wpa_supplicant
bash service wpa_supplicant stop sudo systemctl mask wpa_supplicant.service sudo update-rc.d dhcpcd disable

# Disable and configure wlan0
ip link set wlan0 down
iw wlan0 set type ibss
# ifconfig wlan0 mtu 1532 # Invalid argument?
iwconfig wlan0 mode ad-hoc
# iwconfig wlan0 essid $ESSID # Guess this is redundant
iwconfig wlan0 channel $CHANNEL
ip link set wlan0 up
iw wlan0 ibss join $ESSID 2432 # key d:2:$PWD

# Activate batman-adv
modprobe batman-adv
batctl if add wlan0
ip link set up dev wlan0
ip link set up dev bat0
ifconfig bat0 $IP_ADDRESS

# Start the tools for network visualization
alfred -i bat0 -m -p 1 &
batadv-vis -i bat0 -s &