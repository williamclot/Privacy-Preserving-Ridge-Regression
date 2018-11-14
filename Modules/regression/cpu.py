#!/usr/bin/env python3

'''Ridge Regression on CPU dataset test using Python (pandas & numpy)'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "12/11/2018"

import pandas as pd
import numpy as np
import math
import sys

# System import classes folder as well
sys.path.insert(0,'./classes/')

import Regression as rd
from termcol import termcol as tc

##--------* Regression *---------##

def prepareValues(train_frac=0.8, verbose=False):
    '''
    Function to prepare the values of the dataset before calling the Regression Class
    '''
    print(tc.WARNING+ "--> Preparing the dataset for training..."+ tc.ENDC)
    # Opening up the dataset using pandas to easily manipulate Dataframe variables
    if(verbose): print(tc.HEADER + "  Opening up the CPU dataset..."+tc.ENDC)
    file = r'../../Datasets/machine.data'
    dataset = pd.read_table(file, sep=",")
    if(verbose): print(dataset.head(5))
    
    # Randomizing the rows of the dataset (separation between training a testing dataset)
    if(verbose): print(tc.HEADER + "  Shuffling the index of the dataset..."+tc.ENDC)
    dataset = dataset.sample(frac=1).reset_index(drop=True)
    if(verbose): print(dataset.head(5))

    # Extracting useful data (X, Y)
    data_lenght = dataset.shape[0]
    Y = dataset[['ERP']]
    meanY = float(Y.mean().values)
    X = dataset.drop(columns=['ERP','PRP','vendor name', 'model name'])
    # # Separation between train dataset and test dataset with train_frac
    index_separation = int(data_lenght * train_frac)
    Xtrain = X.iloc[:index_separation]
    Ytrain = Y.iloc[:index_separation]
    Xtest = X.iloc[index_separation:]
    Ytest = Y.iloc[index_separation:]

    return Xtrain, Ytrain, Xtest, Ytest, meanY


# Preparing the values and initiating the regression class
# ----------------------------------------------------------
X, Y, Xtest, Ytest, meanY = prepareValues(verbose=True)
Regression = rd.Regression(X, Y, verbose=True, unified=False)

# # Training the model with X and Y sets
# # -------------------------------------
print(tc.WARNING+ "--> Training our regression model..."+ tc.ENDC)
Regression.train_model()
print(tc.OKGREEN+ "  Training phase of the model finished!"+ tc.ENDC)
print(tc.OKGREEN+ "  Output model of the training (beta) :"+ tc.ENDC)
print(Regression.beta)

# # Training the model with X and Y sets
# # -------------------------------------
print(tc.WARNING+ "--> Testing the model with the last 20% of the dataset!"+ tc.ENDC)
average_error = Regression.test_model(Xtest, Ytest)
print(tc.OKGREEN+ "  Average error :"+ tc.ENDC, average_error)
print(tc.OKGREEN+ "  Y average value :"+ tc.ENDC, meanY)
print(tc.OKGREEN+ "  Ymax value :"+ tc.ENDC, float(Regression.Ymax))
print(tc.OKGREEN+ "  Ymin value :"+ tc.ENDC, float(Regression.Ymin))
print(tc.OKGREEN+ "  Relative error :"+ tc.ENDC, float(average_error/meanY))