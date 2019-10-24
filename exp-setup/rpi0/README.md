## Setup Picamera and MQTT Client on Raspberry Pi Zero

1. Install camera on RPi, enable camera in raspi-config.

   Use the following command to install `picamera` module for Python3, if necessary:

   ```shell
   sudo apt-get install python3-picamera
   ```

2. Install `paho-mqtt`:

   ```shell
   sudo apt install python3-pip
   sudo pip3 install paho-mqtt
   ```