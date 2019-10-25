## Setup MQTT, Scikit-Learn, Keras on Raspberry Pi 3B

### MQTT Broker and Client

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

   To start the broker, use the following command to let the broker start listen on port <port> with verbose:

   ```shell
   mosquitto -p <port> -v
   ```

   On the client side, to publish a topc, use [mosquitto_pub](https://mosquitto.org/man/mosquitto_pub-1.html).

   ```shell
   mosquitto_pub -h <hostname> -p <port> -u <username> -P <password> \ 
   -t topic -i <client_id> -k <keepalive> -q <qos> \
   { -f file | -l | -m message | -n | -s }
   ```

   To subscribe a topic, use [mosquitto_sub](https://mosquitto.org/man/mosquitto_sub-1.html).
   
   ```shell
   mosquitto_sub -h <hostname> -p <port> -u <username> -P <password> \
   -t topic -i <client_id> -k <keepalive> -q <qos>
   ```
   
4. **To run the script in this folder**

   After starting the mosquitto broker on localhost (i.e. on this RPi 3B), run the following script to 1) connect to the broker, 2) subscribe the RPi0 image topic and save the image when receives.

   ```shell
   python3 mqtt_sub.py
   ```

### Scikit-Learn

1. Installation on Raspberry Pi.

   ```shell
   pip3 install scikit-learn
   ```

2. Other required modules: `matplotlib` and `numpy`:

   ```shell
   pip3 install matplotlib
   pip3 install numpy
   ```

3. 

### Keras

Although we end up with using `scikit-learn` instead of Keras, the installation and a simple example of Keras is noted here.

1. Install Keras on Raspberry Pi. Follow the tutorial [here](https://medium.com/@abhizcc/installing-latest-tensor-flow-and-keras-on-raspberry-pi-aac7dbf95f2) to install tensorflow and Keras.
   Note you can download the latest tensorflow compatible with the Python version, from the [release page](https://github.com/lhelontra/tensorflow-on-arm/releases/) provided by [lhelontra](https://github.com/lhelontra). In this case, *tensorflow-1.14.0-cp35-none-linux_armv7l.whl* for  Raspberry pi 2/3 is selected. 

2. A simple example of Keras on Raspberry Pi is the MNIST classification. Run the script in this folder to test:

   ```shell
   python3 keras_mnist.py
   ```

   