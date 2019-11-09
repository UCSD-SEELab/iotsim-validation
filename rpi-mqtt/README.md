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
   
3. **To run the script in this folder**

   After starting the mosquitto broker on localhost (i.e. on RPi 3B), set the IP address and port. Then run the following script to continuously take photos (every 500ms) and send to broker.

   ```shell
   python3 main.py 0.5
   ```
   
   If you want to control the resolution of the picture through command line, use the following one to take 1024*1024 images:
   
   ```shell
   python3 main.py 0.5 1024 1024
   ```
   
   **Note**: take one picture of 128*128 takes approximately 0.05s, while 1024\*1024 takes 0.3-0.4s. The **default resolution** is 512\*512. 