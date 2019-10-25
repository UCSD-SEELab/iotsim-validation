#!/usr/bin/python3

'''
Example module to receive picture from Raspberry Pi
Zero via MQTT. Call the procssing function if required.
Send the raw image or the processed result to broker.
Work on Python 3.5.3 of Raspberry Pi 3B+

To run without processing:
    python3 mqtt.py
To run with processing, hidden layer (5, 10)
    python3 -p -l 5 10
Author: Xiaofan Yu
Date: 10/23/2019
'''
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import argparse
from mlp import infer
MQTT_SERVER = 'localhost'
MQTT_PORT = 1884

class myMQTTReceiver():
    def __init__(self, server_ip=None, server_port=None, \
            client_id='rpi3b', sub_topic=None, \
            process=False, hidden_layer=None):
            '''
            Args:
                server_ip, server_port: ip and port of broker
                client_id: client id of this rpi 3b
                sub_topic: the list of topic that this device subscribes
                process: whether processing the image before publish
                hidden_layer: the number of units in each hidden layer of
                    MLP, if process the image
            '''
            self.hostname = server_ip
            self.port = server_port
            self.client = mqtt.Client(client_id=client_id)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect(host=self.hostname, port=self.port)
            self.sub_topic = sub_topic
            self.process = process
            self.hidden_layer = hidden_layer
            self.qos = 0
            self.img_path = './output.jpg'


    # The callback for when the client receives a CONNACK response
        # from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the
            # connection and reconnect then subscriptions will be renewed.
            # Note that self.sub_topic can be a list
        self.client.subscribe(self.sub_topic)


    def on_message(self, client, userdata, msg):
        # process for different topics
        if msg.topic == 'rpi0/img':
            print("Image Received")
            # if no processing here, directly forward the data
            if not self.process:
                self.client.publish('rpi3b/img', msg.payload)
            else:
                # write down the image
                with open(self.img_path, 'wb') as f:
                    f.write(msg.payload)
                    f.close()

                # process the image and publish the result
                payload = infer(self.img_path, self.hidden_layer)
                payload = bytearray(payload)
                self.client.publish('rpi3b/img', payload)
            print("Image Published")


def main():
    # parse the parameters
    parser = argparse.ArgumentParser(description='Run MQTT client to receive \
            image and process it locally if specified')
    parser.add_argument('-p', '--process', type=bool, dest='process', \
            default=False, help='Whether run local processing')
    parser.add_argument('-l', '--layer', type=int, nargs='+', dest='layer', \
            default=None, help='Specify the number of nodes in each hidden layer')

    args = parser.parse_args()
    print(args.process, args.layer)
    if args.process:
        args.layer = tuple(args.layer)

    # start MQTT client
    mqttRev = myMQTTReceiver(server_ip=MQTT_SERVER, server_port=MQTT_PORT, \
                sub_topic='rpi0/img', process=args.process, \
                hidden_layer=args.layer)
    mqttRev.client.loop_forever()

if __name__ == '__main__':
    main()
