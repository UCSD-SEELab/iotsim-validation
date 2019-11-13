#!/usr/bin/python3

'''
A bridge to connect ESP8266 mesh and RPi mesh.
    1) act as a MQTT server and receive all the message from ESP8266s.
    2) act as a MQTT client, forward esp's data to broker.
Work on Python 3.5.3 of Raspberry Pi Zero

To start the bridge, simply run the script.
    python3 mqtt_bridge.py

Author: Xiaofan Yu
Date: 11/8/2019
'''
import paho.mqtt.client as mqtt
import time
import sys

client_pi = None
client_esp = None
'''
This section is for connecting to center pi broker.
Act as a MQTT client.
'''
# The callback for when the client receives a CONNACK response from the server.
def on_connect_pi(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe('cmd') # subscribe cmd topic

def on_message_pi(client, userdata, msg):
    # simply forward all the incoming cmd messages, from pi broker to esp
    print("Received from pi broker:" + msg.topic + " " + str(msg.payload))
    global client_esp
    try:
        client_esp.publish(topic=msg.topic, payload=msg.payload)
    except Exception as e:
        print(e)

broker_IP = '172.27.0.1'
broker_port = 61613

client_pi = mqtt.Client("Bridge")
client_pi.connect(broker_IP, broker_port, 60)
client_pi.on_connect = on_connect_pi
client_pi.on_message = on_message_pi
client_pi.loop_start() # nonblocking version

'''
This section is for forwarding ESP8266's msg.
Act as a MQTT server.
'''
# The callback for when the client receives a CONNACK response from the server.
def on_connect_esp(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("status/#") # subscribe status topic
    client.subscribe("data/#") # subscribe data topic

def on_message_esp(client, userdata, msg):
    # simply forward all the incoming messages, from esp to pi broker
    print("Received from ESP:" + msg.topic + " " + str(msg.payload))
    global client_pi
    topic = msg.topic.split('/')
    if topic[0] == 'data':
        # format the data topic, add time stamp to payload (power data of ESPs)
        data_payload = str(time.time()) + ',' + msg.payload.decode('utf-8')
        data_payload = data_payload.encode('utf-8')
        try:
            client_pi.publish(topic=msg.topic, payload=data_payload)
            print("forward data from {}".format(msg.topic))
        except Exception as e:
            print(e)
    else: # topic[0] == 'status':
        # simply forward all ready msg
        try:
            client_pi.publish(topic=msg.topic, payload=msg.payload)
            print("forward status msg: {}:{}".format(msg.topic, msg.payload))
        except Exception as e:
            print(e)

# connect to the broker of ESPs
server_IP = '192.168.1.46' # localhost
server_port = 61613
client_esp = mqtt.Client("Bridge")
client_esp.connect(server_IP, server_port, 60)
client_esp.on_connect = on_connect_esp
client_esp.on_message = on_message_esp
client_esp.loop_forever() # nonblocking version
