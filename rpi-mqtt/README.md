# Setup a Raspberry Pi node as MQTT client

Note: to use the scripts in this foler, installation of INA219 and paho-mqtt are required, both of which are included `rpi-mesh-setup/install.sh`.

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
   
3. To run the script in this folder

   To start the client, there are at least 2 parameters you need to specify as command line arguments: 

   * the IP of the client, e.g. 172.27.0.2.
   * the interval you want the lient to send power/temp data, e.g. 0.2s.
   * Running every second, feed 1000kB to Linear Regression and publish 1KB after it. 
   * The total execution time of the client, e.g. 300s.

   **Before start the client, remember to double check whether setting the address of INA219 sensors correctly!**

   The following command is an example with the above settings:

   ```shell
   python3 mqtt_client.py 172.27.0.2 1000 1 300
   ```

   