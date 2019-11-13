# Data Collection on Raspberry Pi Broker

## Experiment Procedure

1. Start broker on Pi broker (172.27.0.1).

   ```shell
   mosquitto /home/pi/iotsim-validation/rpi-broker/mosquitto-wlan0.conf -p 61613 -v
   ```

2. Power up/reset all ESP8266s. Check on Pi broker to ensure that every ESP is ready.

3. Start the experiment by running script:

   ```shell
   python3 start_exp.py 0.2 1000 300
   ```

   Here, the first parameter refers to power & temperature sampling interval on Pi's, 0.2s in this example.  The second parameter means every Pi client will try to send 1000 bytes of fake data to broker every second. The last parameter is the total experiment time in seconds, 300s in this case.