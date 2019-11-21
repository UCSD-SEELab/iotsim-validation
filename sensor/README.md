# Sensors and their interacting script used in this setup

We have current sensor [INA219](#INA219) and temperature & humidity sensor [DHTxx](#DHTxx).

## INA219

### Installation

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
   python3 ina219-pi.py
   ```

3. Use functions `read_power()`, `read_voltage()`, `read_current` in `ina219-pi.py` for INA219 readings.

### Resources

[Official tutorial by Adafruit](https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/overview): wiring, Arduino code, CircuitPython.

[pi-ina219 library on PyPI](https://pypi.org/project/pi-ina219/): this is the Python library used in our setting.

## DHTxx

### Installation

You can either install it with `pip3` with `pip3 install Adafruit-DHT`, or install it from [Github source](https://github.com/adafruit/Adafruit_Python_DHT).

### Setup on Pi

[Setup DHT11 on RPI](http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/)

[Setup DHT22 on RPi](https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/).

DHTxx can be power with 3-5v. In default, the signal pin is connected to **GPIO7**, which is noted as **GPIO4** in BCM standard.

The example script in this directory is directly copied from the Github. To run it with DHT22 connected to GPIO4 (BCM), use:

```shell
python3 AdafruitDHT.py 22 4
```