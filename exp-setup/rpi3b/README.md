1. Install `paho-mqtt`:

   ```shell
   sudo apt install python3-pip
   sudo pip3 install paho-mqtt
   ```

2. Install mosquitto server:

   ```shell
   sudo apt update
   sudo apt install -y mosquitto mosquitto-clients
   
   # to make mosquitto auto start on boot up
   sudo systemctl enable mosquitto.service
   ```

3. To use mosquitto:

   To start the broker, use the following command to let the broker start listen on port <port>.

   ```shell
   mosquitto -p <port> -v
   ```

