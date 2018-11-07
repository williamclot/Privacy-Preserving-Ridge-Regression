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

def prepareValues(train_frac=0.8):
    '''
    Function to prepare the values of the dataset before calling the Regression Class
    '''
    print(termcol.HEADER + "Opening up the dataset..."+termcol.ENDC)
    # Opening up the dataset and extracting useful data (X, Y)
<<<<<<< HEAD
    dataset = pd.read_csv("../../Datasets/forestfires.csv")
    # Randomizing the rows of the dataset (separation between training a testing dataset)
    print(termcol.HEADER + "Opening up the dataset..."+termcol.ENDC)
    dataset = dataset.sample(frac=1).reset_index(drop=True)
>>>>>>> e048b42f0ba8dee1b35b0197ebadc6d9f8bef223

    Y = dataset[['area']]
    # Applying the log model to the area using pandas apply() function
    Y = Y.apply(lambda x: np.log(x + 1))

    X = dataset[['FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain']]

    # Separation between train dataset and test dataset
    data_lenght = dataset.shape[0]
    index_separation = int(data_lenght * train_frac)

    return X.iloc[:index_separation], Y.iloc[:index_separation], X.iloc[index_separation:], Y.iloc[index_separation:] 


X, Y, Xtest, Ytest = prepareValues()
Regression = rd.Regression(X,Y)
Regression.train_model()

print(termcol.WARNING+ "beta :"+ termcol.ENDC)
print(Regression.beta)


result = Regression.test_model(Xtest,Ytest)
print(result)


# print(termcol.WARNING+ "A*beta :"+ termcol.ENDC)
# print(np.dot(Regression.A, Regression.beta))
# # assert(np.dot(Regression.A, Regression.beta) == Regression.b)
# print(termcol.WARNING+"b :"+ termcol.ENDC)
# print(Regression.b)