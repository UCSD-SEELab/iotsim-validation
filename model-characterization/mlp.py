#!/usr/bin/python3

'''
Run MLP to process image on Raspberry Pi 3B.
Work on Python 3.5.3 of Raspberry Pi 3B+.
To train a model with (5,2) hidden layer on output.jpg:
    python3 mlp.py -m train -l 5 2 -p ./output.jpg
To infer an image with (5,2) hidden layer on output.jpg for 10 times:
    python3 mlp.py -m infer -l 5 2 -p ./output.jpg -t 10

Author: Xiaofan Yu
Date: 10/24/2019
'''
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import argparse
import time
import socket

UDP_IP = "169.254.209.38"
UDP_PORT = 5005
ST_MSG = b'start'
FI_MSG = b'stop'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
model_dir = '/home/pi/iotsim-validation/model-characterization/models/'

def read_img(img_path):
    '''
    The input image should be (128, 128, 3)
    while will be resize into (1, 49152)
    '''
    #X = plt.imread(img_path)
    X = np.random.normal(size=(128, 128))
    X = X.reshape((1, -1))
    # print(X.shape)
    return X

def train_model(img_path, hidden_layer):
    '''
    Use one image-output to train the model of
    certain structure. Save model.
    '''
    X = read_img(img_path)
    y = [1, ] # just random
    clf = MLPClassifier(hidden_layer_sizes=hidden_layer)
    clf.fit(X, y)
    # save model
    model_name = model_dir + '{}-{}.sav'.format(X.shape, hidden_layer)
    pickle.dump(clf, open(model_name, 'wb'))
    print('Train model and save to {}'.format(model_name))
    print('MAC operations: {}'.format(MAC(img_path, hidden_layer, 1)))

def infer(img_path, hidden_layer):
    '''
    Load model and infer the result incoming image.
    '''
    X = read_img(img_path)
    model_name = model_dir + '{}-{}.sav'.format(X.shape, hidden_layer)
    if not os.path.exists(model_name):
        raise Exception('No available model {}!'.format(model_name))
    clf = pickle.load(open(model_name, 'rb'))
    return clf.predict(X)

def MAC(img_path, hidden_layer, output_size):
    '''
    calculate the number of MAC operations
    '''
    X = read_img(img_path)
    # convert all the sizes to one list
    input_size = X.size
    l = [input_size]
    l.extend(list(hidden_layer))
    l.append(output_size)
    # print(l)
    mac = 0
    for i in range(len(l)-1):
        mac += l[i]*l[i+1]
    return mac

def main():
    '''
    Run train or inference according to arguments.
    '''
    # parse the parameters
    parser = argparse.ArgumentParser(description='Run MLP training or \
            inference on image.')
    parser.add_argument('-m', '--mode', type=str, dest='mode', \
            help='Specify \'train\' or \'infer\' mode.')
    parser.add_argument('-l', '--layer', type=int, nargs='+', dest='layer', \
            help='Specify the number of nodes in each hidden layer.')
    parser.add_argument('-p', '--path', type=str, dest='path', \
            help='The path of the image.')
    parser.add_argument('-t', '--times', type=int, dest='times', default=1, \
            help='Number of times to run inference.')

    args = parser.parse_args()

    # print(args.mode, args.layer, args.path)
    if args.mode == 'train':
        hidden_layer = tuple(args.layer)
        train_model(args.path, hidden_layer)
    elif args.mode == 'infer':
        sock.sendto(ST_MSG, (UDP_IP, UDP_PORT))
        st_time = time.time()
        for i in range(args.times):
            infer('output.jpg', tuple(args.layer))
        run_time = time.time() - st_time
        sock.sendto(FI_MSG, (UDP_IP, UDP_PORT))
        mac = MAC('output.jpg', tuple(args.layer), 1)
        print(run_time, mac)
    else:
        raise Exception('This mode is not supported!')

if __name__=='__main__':
    main()

