# Setup MQTT, Scikit-Learn, Keras on Raspberry Pi 3B

[Environment Setup](#Environment-Setup)

[Run Instructions](#Run-Instructions)

## Environment Setup

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
   

### Scikit-Learn

1. Installation on Raspberry Pi.

   ```shell
   sudo apt-get install gfortran libgfortran3 libatlas-base-dev libopenblas-dev liblapack-dev -y
   sudo pip3 install scikit-learn
   ```

2. Other required modules: `matplotlib` and `numpy`:

   ```shell
   sudo pip3 install matplotlib
   sudo pip3 install numpy
   ```
   
3. **Important:** sometimes installing through `pip` will cause import errors (guess this is some version control issues). Instead, you can use `apt` to install stable versions as follows.

   ```shell
   sudo apt-get install python3-numpy python3-matplotlib python3-scipy
   ```

### Keras (Optional)

Although we end up with using `scikit-learn` instead of Keras, the installation and a simple example of Keras is noted here.

1. Install Keras on Raspberry Pi. Follow the tutorial [here](https://medium.com/@abhizcc/installing-latest-tensor-flow-and-keras-on-raspberry-pi-aac7dbf95f2) to install tensorflow and Keras.
   Note you can download the latest tensorflow compatible with the Python version, from the [release page](https://github.com/lhelontra/tensorflow-on-arm/releases/) provided by [lhelontra](https://github.com/lhelontra). In this case, *tensorflow-1.14.0-cp35-none-linux_armv7l.whl* for  Raspberry pi 2/3 is selected. 

2. A simple example of Keras on Raspberry Pi is the MNIST classification. Run the script in this folder to test:

   ```shell
   python3 keras_mnist.py
   ```

## Preparation

You need to train the MLP model for every input-hidden layer-output (fix to 1) combination.

To train a model with (5,2) hidden layer on `output.jpg`:

```shell
python3 mlp.py -m train -l 5 2 -p output.jpg
```

To infer an image with the model obtained in the above training:

```shell
python3 mlp.py -m infer -l 5 2 -p output.jpg
```

## Run Instructions

1. Start the mosquitto broker

   ```shell
   mosquitto -p 61613 -v
   ```

2. Start the receiver client on Raspberry Pi 3B, specifying whether perform local processing:

   Do local image processing with a MLP with hidden layers (5,10), run Linear Regression of 18 inputs and 10 outputs at the same time:

   ```shell
   python3 mqtt.py -ip 1 -il 5 10 -pp 1 -pl 18 10
   ```

   Do not process locally. Instead, directly forward the image:

   ```shell
   python3 mqtt.py
   ```

3. Trigger the image publishing on Raspberry Pi zero. The image is set to a resolution of 1024*1024, with an interval of 0.5s.

   ```shell
   python3 main.py 0.5 1024 1024 # in ./rpi0
   ```

   