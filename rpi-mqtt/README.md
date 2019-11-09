# Setup a Raspberry Pi node as MQTT client

[Setup INA219](#Setup-INA219)

[Setup MQTT Client on Raspberry Pi Zero](#Setup-MQTT-Client-on-Raspberry-Pi-Zero)

## Setup INA219

### Requirements

**Remember to enable ssh and I2C interface in `raspi-config`.**

The following operations needs internet connection.

1. Install `pip3`.

   ```shell
   sudo apt install python3-pip
   ```

2. Install `pi-ina219` module.

   ```
   pip3 install pi-ina219
   ```

### Setup on RPi

1. Connect INA219 to RPi. Check through `i2cdetect`:

   ```shell
   pi@raspberrypi:~/$ sudo apt-get install -y i2c-tools
   pi@raspberrypi:~/$ i2cdetect -y 1
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
   00:          -- -- -- -- -- -- -- -- -- -- -- -- --
   10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   40: -- -- -- -- 44 -- -- -- -- -- -- -- -- -- -- --
   50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   70: -- -- -- -- -- -- -- --
   ```

   You should be able to see the address of your INA219, which is 0x44 in this case.

2. Install `pi-ina219` and try the power-print script `ina219-pi.py` in this directory. Remember to change the address and range setting if necessary.

   ```shell
   pip3 install pi-ina219
   python3 ina219_pi.py
   ```

3. Use functions `read_power()`, `read_voltage()`, `read_current` in `ina219-pi.py` for INA219 readings.

### Resources

[Official tutorial by Adafruit](https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/overview): wiring, Arduino code, CircuitPython.

[pi-ina219 library on PyPI](https://pypi.org/project/pi-ina219/): this is the Python library used in our setting.

## Setup MQTT Client on Raspberry Pi Zero

2. Install `paho-mqtt`:

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

   