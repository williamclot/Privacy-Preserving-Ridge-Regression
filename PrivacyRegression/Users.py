#!/usr/bin/env python3

'''Users Class for the Privacy Preserving Ridge Regression'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "13/11/2018"

import pandas as pd
from phe import paillier
import numpy as np
import math
import sys
import socket, pickle

# System import classes folder as well
sys.path.insert(0,'./classes/')

from utils import termcol as tc
from utils import utils
from utils import members
u = utils();

##---------* Functions *----------##

class Users:
    def __init__(self, verbose=False, encrypt=True):
        # Programm parameters
        self.verbose = verbose

        if (self.verbose):
            print(tc.WARNING+"Initiating the Users [-]"+tc.ENDC)

        self.public_key = u.receiveViaSocket(members.Users, "\t --> Receiving public key from CSP")

        print(self.public_key)
        print(self.public_key.encrypt(2))

        u.sendViaSocket(members.CSP, self.public_key.encrypt(2))


    def prepareValues(train_frac=0.8, verbose=False):
        '''
        Function to prepare the values of the dataset before calling the Regression Class
        '''
        # Opening up the dataset using pandas to easily manipulate Dataframe variables
        print(tc.HEADER + "Opening up the dataset..."+tc.ENDC)
        file = r'../Datasets/Concrete_Data.xlsx'
        dataset = pd.read_excel(file)
        if(verbose): print(dataset.head(5))
        
        # Randomizing the rows of the dataset (separation between training a testing dataset)
        print(tc.HEADER + "Shuffling the index of the dataset..."+tc.ENDC)
        dataset = dataset.sample(frac=1).reset_index(drop=True)
        if(verbose): print(dataset.head(5))

        # Extracting useful data (X, Y)
        data_lenght = dataset.shape[0]
        Y = dataset[['Strength']]
        X = dataset.drop(columns=['Strength', 'Superplasticizer'])
        # Separation between train dataset and test dataset with train_frac
        index_separation = int(data_lenght * train_frac)
        Xtrain = X.iloc[:index_separation]
        Ytrain = Y.iloc[:index_separation]
        Xtest = X.iloc[index_separation:]
        Ytest = Y.iloc[index_separation:]

        return Xtrain, Ytrain, Xtest, Ytest

    def encrypt(self, A, b):
        '''return c = Cpkcsp(A, b)'''
        encrypt_func = lambda plain_text: self.public_key.encrypt(plain_text)
        vector_func = np.vectorize(encrypt_func)

        return [vector_func(A), vector_func(b)]

            
Users = Users(verbose=True, encrypt=False)




        

            
       





