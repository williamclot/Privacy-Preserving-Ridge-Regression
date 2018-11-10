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

def prepareValues(train_frac=0.8, verbose=False):
    '''
    Function to prepare the values of the dataset before calling the Regression Class
    '''
    # Opening up the dataset using pandas to easily manipulate Dataframe variables
    print(termcol.HEADER + "Opening up the dataset..."+termcol.ENDC)
    file = r'../../Datasets/Concrete_Data.xlsx'
    dataset = pd.read_excel(file)
    if(verbose): print(dataset.head(5))
    
    # Randomizing the rows of the dataset (separation between training a testing dataset)
    print(termcol.HEADER + "Shuffling the index of the dataset..."+termcol.ENDC)
    dataset = dataset.sample(frac=1).reset_index(drop=True)
    if(verbose): print(dataset.head(5))

    # Extracting useful data (X, Y)
    data_lenght = dataset.shape[0]
    Y = dataset[['Strength']]
    print(Y)
    X = dataset.iloc[0:data_lenght-3]

    # Separation between train dataset and test dataset with train_frac
    index_separation = int(data_lenght * train_frac)
    Xtrain = X.iloc[:index_separation]
    Ytrain = Y.iloc[:index_separation]
    Xtest = X.iloc[index_separation:]
    Ytest = Y.iloc[index_separation:]

    return Xtrain, Ytrain, Xtest, Ytest


X, Y, Xtest, Ytest = prepareValues(verbose=True)
print(Y)
Regression = rd.Regression(X,Y,verbose=True)
# Regression.train_model()

# print(termcol.WARNING+ "beta :"+ termcol.ENDC)
# print(Regression.beta)


# result = Regression.test_model(Xtest,Ytest, func = lambda x: np.exp(x)-1)
# print(result)