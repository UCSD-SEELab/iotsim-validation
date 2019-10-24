#!/usr/bin/python3

'''
Example module to receive picture from Raspberry Pi
Zero via MQTT.
Work on Python 3.5.3 of Raspberry Pi 3B+

Author: Xiaofan Yu
Date: 10/23/2019
'''
import paho.mqtt.client as mqtt
MQTT_SERVER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "rpi0/img"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)
    # The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    # more callbacks, etc
    # Create a file with write byte permission
    f = open('./output.jpg', "wb")
    f.write(msg.payload)
    print("Image Received")
    f.close()

client = mqtt.Client(client_id='rpi3b')
client.on_connect = on_connect
client.on_message = on_message
client.connect(host=MQTT_SERVER, port=MQTT_PORT, keepalive=60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()