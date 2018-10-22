#!/usr/bin/env python3

""""Ridge Regression test using Python (pandas & numpy)"""

__author__ = "William CLOT, williamclot.github.com"
__license__ = "MIT"
__date__ = "22/10/2018"

import pandas as pd
import numpy as np
import math

##---------* Functions *----------##

def opendata(url):
    return pd.read_csv(url)

def getA(X, lamb=0.1):
    '''get A from X and lambda'''
    d = len(X[0])
    I = np.eye(d)
    Xt = np.transpose(X)

    A = np.dot(Xt, X)+lamb*I

    return A, Xt

def getb(Xt, Y):
    '''get b from Xt and Y'''
    b = np.dot(Xt, Y)

    return b


##--------* Regression *---------##

data = opendata("./../../datasets/forestfires.csv")

Y = data[['area']].values

# Applying the logarithm model to the area
for i in range(len(Y)):
    Y[i] = math.log(Y[i]+1)

X = data[['FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain']].values

A, Xt = getA(X)
b = getb(Xt, Y)

print(A)