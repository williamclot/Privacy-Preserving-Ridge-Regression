#!/usr/bin/env python3

'''Privacy Preserving Ridge Regression'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "13/11/2018"

import pandas as pd
import numpy as np
import math
import sys

# System import classes folder as well
sys.path.insert(0,'./classes/')

import Evaluator
import Users
import CSP

from termcol import termcol as tc

##--------* Global variables *----------##

VERBOSE = True
CSP_Key = ''
LAMBDA = 0.1

##--------* Initiating the database *---------##

def prepareValues(train_frac=0.01, verbose=False):
    '''
    Function to prepare the values of the dataset before calling the Regression Class
    '''
    # Opening up the dataset using pandas to easily manipulate Dataframe variables
    print(tc.HEADER + "Opening up the dataset..."+tc.ENDC)
    file = r'../Datasets/Concrete_Data.xlsx'
    dataset = pd.read_excel(file)
    if(verbose): print(dataset.head(5))
    
    # Randomizing the rows of the dataset (separation between training a testing dataset)
    # print(tc.HEADER + "Shuffling the index of the dataset..."+tc.ENDC)
    # dataset = dataset.sample(frac=1).reset_index(drop=True)
    # if(verbose): print(dataset.head(5))

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

if (VERBOSE): print(tc.WARNING+"Initiating the Privacy Preserving Ridge Regression Programm..."+tc.ENDC)

Xtrain, Ytrain, Xtest, Ytest = prepareValues(verbose=VERBOSE)


##--------* Initiating the actors *---------##


CSP = CSP.CSP(verbose=VERBOSE)
CSP_Key = CSP.public_key #Getting the generated public key

Users = Users.Users(CSP_Key, Xtrain, Ytrain, verbose=VERBOSE)
Evaluator = Evaluator.Evaluator(CSP_Key, Users.c, LAMBDA, verbose=VERBOSE)
A_enc = Evaluator.A_enc
A_dec = CSP.decrypt(A_enc)
print(A_dec)


