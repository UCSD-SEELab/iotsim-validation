#!/bin/sh -e
# Set up a RPi 3B as a gateway in a mesh network.
# Compile and install batman-adv, batctl.
# Configure mesh network.
#
# Author: Xiaofan Yu
# Date: 11/5/2019
ESSID="my-mesh"
PWD="goodluck"
CHANNEL=3
IP_ADDRESS=172.27.0.1/16

apt install libnl-3-dev libnl-genl-3-dev

cd /home/pi
git clone https://git.open-mesh.org/batctl.git
cd batctl
make install

# Disable and configure wlan0
ip link set wlan0 down
iw wlan0 set type ibss
ifconfig wlan0 mtu 1532
iwconfig wlan0 mode ad-hoc
iwconfig wlan0 essid $ESSID
iwconfig wlan0 channel $CHANNEL
ip link set wlan0 up
iw wlan0 ibss join $ESSID 2432 key d:2:$PWD

# Activate batman-adv
modprobe batman-adv
batctl if add wlan0
ip link set up dev wlan0
ip link set up dev bat0
ifconfig bat0 $IP_ADDRESS
