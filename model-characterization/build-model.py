#!/usr/bin/python

'''
Python 2.7 script on the host Pi for power measuring and model fitting.

Author: Xiaofan Yu
Date: 10/14/2019
'''
import sys
import os
import time
#import powermeter
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def run_workload(platform, workload, **kwargs):
    pass

def MSE(X, Y):
    '''
    Compute the mean square error of X and Y

    Args:
        X, Y (n*1 float array): two arrays to compare

    Returns:
        MSE (float): mean square error
    '''
    X, Y = np.array(X), np.array(Y)
    assert(X.shape == Y.shape), "MSE: X and Y does not match!"

    MSE = np.square(np.subtract(X, Y)).mean()
    return MSE

def fit_linear(data_size, value):
    '''
    Try to fit the value-input data size model with Linear Regression
    The value here can be avg power or exec. time.

    Args:
        data_size (n*1 int array): the size of the input data in kB
        value (n*1 float array): the target value of regression

    Returns:
        popt (float array): opt. coefficients
        mse (float): Mean Square Error
    '''
    data_size, value = np.array(data_size), np.array(value)
    assert (data_size.shape[0] == value.shape[0]), \
            "fit_linear: input dimension does not match!"
    if len(data_size.shape) == 1: # if data_size is 1d, expand to 2d
        data_size = data_size.reshape(-1, 1)

    lg = LinearRegression().fit(data_size, value)

    fit_linear.popt = [lg.coef_, lg.intercept_]
    predict = lg.predict(data_size)
    fit_linear.mse = MSE(value, predict)
    return fit_linear.popt, fit_linear.mse

def fit_poly(data_size, value):
    '''
    Try to fit the value-input data size model with Polynomial Regression
    The value here can be avg power or exec. time.

    Args:
        data_size (n*1 int array): the size of the input data in kB
        value (n*1 int float): the target value of regression

    Returns:
        popt (float array): opt. coefficients
        mse (float): Mean Square Error
    '''
    data_size, value = np.array(data_size), np.array(value)
    assert (data_size.shape[0] == value.shape[0]), \
            "fit_poly: input dimension does not match!"
    if len(data_size.shape) == 1: # if data_size is 1d, expand to 2d
        data_size = data_size.reshape(-1, 1)

    poly = PolynomialFeatures(degree=2)
    dsize_ = poly.fit_transform(data_size)
    lg = LinearRegression().fit(dsize_, value)

    fit_poly.popt = [lg.coef_, lg.intercept_]
    predict = lg.predict(dsize_)
    fit_poly.mse = MSE(value, predict)
    return fit_poly.popt, fit_poly.mse

def fit_exp(data_size, value):
    '''
    Try to fit the value-input data size model with Exponential Regression
    The value here can be avg power or exec. time.

    Args:
        data_size (1-d int array): the size of the input data in kB
        value (1-d int float): the target value of regression

    Returns:
        popt (float array): opt. coefficients
        mse (float): Mean Square Error
    '''
    def exp_func(x, a, b, c):
        return a * np.exp(b * x) + c

    data_size, value = np.array(data_size), np.array(value)
    assert (data_size.shape[0] == value.shape[0]), \
            "fit_exp: input dimension does not match!"

    fit_exp.popt, _ = curve_fit(exp_func, data_size, value)

    predict = exp_func(data_size, *fit_exp.popt)
    fit_exp.mse = MSE(value, predict)
    return fit_exp.popt, fit_exp.mse

def fit_log(data_size, value):
    '''
    Try to fit the value-input data size model with Log Regression
    The value here can be avg power or exec. time.

    Args:
        data_size (1-d int array): the size of the input data in kB
        value (1-d int float): the target value of regression

    Returns:
        popt (float array): opt. coefficients
        mse (float): Mean Square Error
    '''
    def log_func(x, a, b, c):
        return a * np.log(x + b) + c

    data_size, value = np.array(data_size), np.array(value)
    assert (data_size.shape[0] == value.shape[0]), \
            "fit_log: input dimension does not match!"

    fit_log.popt, _ = curve_fit(log_func, data_size, value)

    predict = log_func(data_size, *fit_log.popt)
    fit_log.mse = MSE(value, predict)
    return fit_log.popt, fit_log.mse


def main():
    X = np.array([1.0, 2.0, 3.0, 4.0])
    # X = X.reshape(-1, 1)
    print(X.shape)
    Y = np.array([2.0, 4.0, 8.0, 16.0])
    print(Y.shape)
    popt, mse = fit_log(Y, X)
    print(popt)
    print(mse)

if __name__ == '__main__':
    main()
