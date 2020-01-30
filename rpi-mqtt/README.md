# Raspberry Pi node as a MQTT client

Scripts in this directory are applications running on a RPi which acts as a MQTT client. There are three modules that are required:

* `paho-mqtt` is a Python module to work as a MQTT client.
* `pi-ina219` is a Python module to interact with the current sensor INA219.
* `numpy` is required to run local Linear Regression.

All of the three modules are included in  `rpi-mesh-setup/install.sh`. In other words, by running `rpi-mesh-setup/install`, one node should be ready to run all of the applications as one node in our mesh network.

The following section describes the procedures to setup a client node manually.

## Setup MQTT Client on Raspberry Pi Zero

1. Install `paho-mqtt`:

   ```shell
   sudo apt install python3-pip
   sudo pip3 install paho-mqtt
   ```

2. Install `numpy`:

   ```shell
   pip3 install numpy
   ```
   
3. To run the script in this folder:

   To start the client, there are at least 2 parameters you need to specify as command line arguments: 

   * the IP of the client, e.g. 172.27.0.2.
   * the interval you want the client to send power/temp data, e.g. 0.2s.
   * Running every second, feed 1000kB to Linear Regression and publish 1KB after it. 
   * The total execution time of the client, e.g. 300s.

   **Before start the client, remember to double check whether setting the address of INA219 sensors correctly!**

   The following command is an example with the above settings:

   ```shell
   python3 mqtt_client.py 172.27.0.2 1000 1 300
   ```

   