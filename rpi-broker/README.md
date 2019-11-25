# Data Collection on Raspberry Pi Broker

## Experiment Procedure

1. Start broker on Pi broker (172.27.0.1).

   ```shell
   mosquitto /home/pi/iotsim-validation/rpi-broker/mosquitto-wlan0.conf -p 61613 -v
   ```

3. Start the experiment by running script:

   ```shell
   python3 start_exp.py <test_case> <exec_time>
   ```

   Here, you need to specify the two parameters:
   
   * Name of test case. This will be used for creating data folder and deciding configuration parameters. Options include 'original', 'limit_bw', 'lr', 'limit_bw_lr'. For more details, check the [README](../data/README.md) for data.
   * Total execution time for the experiment. In our tests, we use 5min (i.e. 300s) as the default length.