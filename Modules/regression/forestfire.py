#!/usr/bin/env python3

'''Ridge Regression test using Python (pandas & numpy)'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "22/10/2018"

import pandas as pd
import numpy as np
import math

import Regression as rd

class termcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

##--------* Regression *---------##

def prepareValues():
    '''
    Function to prepare the values of the dataset before calling the Regression Class
    '''
    print(termcol.HEADER + "Opening up the dataset..."+termcol.ENDC)
    # Opening up the dataset and extracting useful data (X, Y)
    dataset = pd.read_csv("../../datasets/forestfires.csv")

    Y = dataset[['area']]
    # Applying the log model to the area using pandas apply() function
    Y = Y.apply(lambda x: np.log(x + 1))

    X = dataset[['FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain']]

    return X, Y


X, Y = prepareValues()
Regression = rd.Regression(X[:int(X.shape[0]*0.8)], Y[:int(Y.shape[0]*0.8)])
Regression.train_model()
result = Regression.test_model(X[int(X.shape[0]*0.8):], Y[int(Y.shape[0]*0.8):])


print(termcol.WARNING+ "beta :"+ termcol.ENDC)
print(Regression.beta)

# print(termcol.WARNING+ "A*beta :"+ termcol.ENDC)
# print(np.dot(Regression.A, Regression.beta))
# # assert(np.dot(Regression.A, Regression.beta) == Regression.b)
# print(termcol.WARNING+"b :"+ termcol.ENDC)
# print(Regression.b)