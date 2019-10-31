#!/usr/bin/python3

'''
Example module to receive picture from Raspberry Pi
Zero via MQTT. Call the procssing function if required.
Send the raw image or the processed result to broker.
Work on Python 3.5.3 of Raspberry Pi 3B+

To run without processing:
    python3 mqtt.py
To run with image processing, hidden layer (5, 10),
Linear Regression on photon data, 18 inputs and 10 outputs:
    python3 -ip 1 -il 5 10 -pp 1 -pl 18 10
Author: Xiaofan Yu
Date: 10/23/2019
'''
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import argparse
from mlp import infer
from lr import LinearRegression
MQTT_SERVER = 'localhost'
MQTT_PORT = 61613

def img_process(payload, *args):
    # process img locally with specified hidden layers
    # write down the image
    hidden_layer = args[0]
    img_path = './output.jpg'
    with open(img_path, 'wb') as f:
        f.write(payload)
        f.close()

    # process the image and publish the result
    payload = infer(img_path, hidden_layer)
    payload = bytearray(payload)
    return payload

def photon_process(payload, *args):
    print(payload)
    payload = payload.decode('utf-8')
    payload = payload.split('[[')
    header = payload[0] # time stamp information
    in_data = payload[1].split(']]')[0]
    in_data = in_data.split(',')
    in_data = [float(d) for d in in_data] # extract the data in float

    assert(photon_process.lr.in_size == in_data)

    out_data = photon_process.lr.run(in_data)
    payload = header + str(out_data)
    payload = bytearray(payload)
    print(payload)

    return payload


class routine():
    def __init__(self, sub_topic: str, pub_topic: str,
                process: bool, func: callable):
        self.sub_topic = sub_topic
        self.pub_topic = pub_topic
        self.process = process
        self.func = func
        self.args = None

img_routine = routine('rpi0/img', 'rpi3b/img', False, None, img_process)
photon_routine = routine('photon/data', 'rpi3b/photon', False, None, photon_process)
receive_routine = [img_routine, photon_routine]

class myMQTTReceiver():
    def __init__(self, server_ip=None, server_port=None, client_id='rpi3b'):
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
        self.qos = 0


    def on_connect(self, client, userdata, flags, rc):
        # The callback for when the client receives a CONNACK response
        # from the server.
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the
        # connection and reconnect then subscriptions will be renewed.
        for r in receive_routine:
            self.client.subscribe(r.sub_topic)
            print("Subscribe topic {}".format(r.sub_topic))


    def on_message(self, client, userdata, msg):
        # process for different topics
        for r in receive_routine:
            if msg.topic == r.sub_topic:
                print('Message of topic {} received'.format(r.sub_topic))
                if not r.process:
                    # if no processing here, directly forward the data
                    self.client.publish(r.pub_topic, msg.payload)
                else:
                    # perform local computation
                    payload = r.func(msg.payload, *r.args)
                    self.client.publish(r.pub_topic, payload)
                print("Message of topic {} published".format(r.pub_topic))
                return


def main():
    # parse the parameters
    parser = argparse.ArgumentParser(description='Run MQTT client to receive \
            data and process it locally if specified')
    parser.add_argument('-ip', '--imageprocess', type=bool, \
            dest='imgprocess', \
            default=False, \
            help='Whether run local image processing')
    parser.add_argument('-il', '--imagelayer', type=int, nargs='+', \
            dest='imglayer', \
            default=None, \
            help='Specify the number of nodes in each hidden layer \
                for MLP used in image processing')
    parser.add_argument('-pp', '--photonprocess', type=bool, \
            dest='photonprocess', \
            default=False, \
            help='Whether run local photon data processing')
    parser.add_argument('-pl', '--photonlayer', type=int, nargs='+', \
            dest='photonlayer', \
            default=None, \
            help='Specify the number of inputs and outputs \
                for Linear Regression used in photon data processing')

    args = parser.parse_args()
    print(args.imgprocess, args.imglayer, args.photonprocess, args.photonlayer)
    try:
        img_routine.process = args.imgprocess
        img_routine.args = tuple(args.imglayer)
        photon_routine.process = args.photonprocess
        photon_routine.args = tuple(args.photonlayer)
    except:
        pass

    # set LinearRegression
    photon_process.lr = LinearRegression(photon_routine.args[0], \
            photon_routine.args[1])

    # start MQTT client
    mqttRev = myMQTTReceiver(server_ip=MQTT_SERVER, server_port=MQTT_PORT)
    mqttRev.client.loop_forever()

if __name__ == '__main__':
    main()
