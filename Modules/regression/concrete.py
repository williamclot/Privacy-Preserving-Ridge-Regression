#!/usr/bin/env python3

'''Ridge Regression test using Python (pandas & numpy)'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "22/10/2018"

import pandas as pd
import numpy as np
import math

import Regression as rd

from termcol import termcol

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
    X = dataset.drop(columns=['Strength'])
    # Separation between train dataset and test dataset with train_frac
    index_separation = int(data_lenght * train_frac)
    Xtrain = X.iloc[:index_separation]
    Ytrain = Y.iloc[:index_separation]
    Xtest = X.iloc[index_separation:]
    Ytest = Y.iloc[index_separation:]

    return Xtrain, Ytrain, Xtest, Ytest


# Preparing the values and initiating the regression class
# ----------------------------------------------------------
X, Y, Xtest, Ytest = prepareValues(verbose=False)
Regression = rd.Regression(X, Y, verbose=False, unified=False)

# Training the model with X and Y sets
# -------------------------------------
Regression.train_model()
print(termcol.OKGREEN+ "Training phase of the model finished!"+ termcol.ENDC)
print(termcol.WARNING+ "Output model of the training (beta) :"+ termcol.ENDC)
print(Regression.beta)

# Training the model with X and Y sets
# -------------------------------------
print(termcol.OKGREEN+ "Testing the model with the last 20% of the dataset!"+ termcol.ENDC)
average_error = Regression.test_model(Xtest,Ytest)
print(termcol.WARNING+ "Average error :"+ termcol.ENDC, average_error)
print(termcol.WARNING+ "Precision :"+ termcol.ENDC, float(average_error/(Regression.Ymax-Regression.Ymin)))