## Setup MQTT Client on Raspberry Pi Zero

1. Install `paho-mqtt`:

```shell
sudo apt install python3-pip
sudo pip3 install paho-mqtt
```

2. **To run the script in this folder**

   To start the client, there are at least 2 parameters you need to specify as command line arguments: 

   * the IP of the client, e.g. 172.27.0.2.
   * the interval you want the lient to send power/temp data, e.g. 0.2s.
   * (Optional) if you want the client to send fake data at the same time, you need to specify the number of bytes to send every second, e.g. 1000 bytes.

   **Before start the client, remember to double check whether setting the address of INA219 sensors correctly!**

   The following command is an example with the above settings:

   ```shell
   python3 mqtt_client.py 172.27.0.2 0.2 1000
   ```

   