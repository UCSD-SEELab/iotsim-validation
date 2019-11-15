# Collected data description

This tutorial will walk you through the organization of experiment data from top to bottom. 

Each folder in this directory contains a set of collected data with specific settings (explained in [Experiment Sets](#Experiment-Sets)). There are 10 `.txt` files in each folder, recording the collected traces from each device (explained in [Devices](#Devices)). Finally, each line in a `.txt` files notes collecting time, power, temperature and delay (explained in [Data Traces](#Data-Traces)). We also provide a script for visualization, see [Instructions for Visualization](#Instructions-for-Visualization).

## Experiment Sets

* **test** - a sample data set collected when all devices are in lab 2115.

  Run by `python3 start_exp.py 0.2 0 1 300`, meaning every client samples every 0.2s, sends 1 Kbytes of fake data into the network each second, and the total experiment runs for 300s.

* **limit_bw** - with 100kbps limited bandwidth between each pair of Pi's.

  Run by `python3 start_exp.py 0.2 0 1 300`, with function `set_bw(100)` called before the experiment starts.

* **lr** - run linear regression workloads (100MB inputs, 10Kbytes outputs) on each device every second.

  Run by `python3 start_exp.py 0.2 100000 10 300`.

* **temp** - with one device heated up by the thermal lamp, thus shows higher ambient temperature.

## Devices

* 172.27.0.1 - this is a Raspberry Pi 3B+ running the central broker. **Note that the power data in this file is wrong.** I don't know why, no matter changing the power wire or another INA219 current sensor, this Pi keeps giving power of less than 1W.
* 172.27.0.2 - 172.27.0.5 - these are Raspberry Pi zeros acting as normal mesh nodes in the network.
* 172.27.0.6 - this is a Raspberry Pi 3B+. Same as RPi zeros, this Pi is also a client connecting to the central broker as a normal mesh node. At the same time, it also serves as a bridge forwarding all data from ESP8266s to the central broker.

## Data Traces

The data in one line in is slightly different for Pi's and ESP's, as we didn't use the internal temperature sensor on ESP8266 due to accuracy issues.

* On **Pi**, the format of one line of data is as follows:

  ```
  time(s), power(mW), temperature(degrees), delay(s)
  ```

* On **ESP8266**, the format of one line is as follows:

  ```
  time(s), power(mW), delay(s)
  ```

  * time - this is the absolute time on Pi that the power & temperature data is collected, obtained by `time.time()`. All Pi's are synchronized.
  * power - this is measured by INA219, which is attached to each device.
  * temperature - on Pi, this is the internal CPU temperature returned by `vcgenmd`.
  * delay - this is the difference between collection time and the time received by the central broker.

## Instructions for Visualization

Run the `plot.py` script in this folder. You need to specify a test case, i.e. a folder. The following command shows an example to visualize 'original' test data.

```shell
python3 plot.py original
```

All plots are stored in the `img` folder, with test case as their name.