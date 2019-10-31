#!/usr/bin/python3

'''
Main script on Raspberry Pi Zero.
Take a picture and send to MQTT broker continuously.
To use the default resolution, take pic every 500ms:
    python3 main.py 0.5
To set resolution in command line, take pic every 500ms:
    python3 main.py 0.5 1024 1024

Author: Xiaofan Yu
Date: 10/23/2019
'''
from camera import myCamera
from mqtt_pub import myMQTTClient
import time
import sys

SERVER_IP = '192.168.1.57'
SERVER_PORT = 61613

def main():
    interval = float(sys.argv[1])
    if len(sys.argv) > 2:
        res = (int(sys.argv[2]), int(sys.argv[3]))
        camera = myCamera(resolution=res)
    else:
        camera = myCamera()
    mqtt = myMQTTClient(server_ip=SERVER_IP, \
        server_port=SERVER_PORT)
    img_path = './image.jpg'

    last_pic = time.time()
    while True:
        remain = interval - (time.time() - last_pic)
        if remain > 0:
            time.sleep(remain)
            print('sleep for %f' %remain)
        camera.capture(sav_path=img_path)
        last_pic = time.time()
        mqtt.pub_img(img_path=img_path)

if __name__ == '__main__':
    main()
