#!/bin/sh -e
# Set up a RPi 3B as a node in a mesh network.
# Compile and install batman-adv, batctl.
# Call scripts to configure the mesh network.
#
# Author: Xiaofan Yu
# Date: 11/5/2019

apt install libnl-3-dev libnl-genl-3-dev
apt install git

if [ ! -f /home/pi/batctl ]; then
	# directory does not exist, then install it
	cd /home/pi
	git clone https://git.open-mesh.org/batctl.git
	cd batctl
	make install
fi