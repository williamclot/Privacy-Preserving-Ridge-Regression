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
from utils import parameters 
from progressbar import ProgressBar
u = utils();

##---------* Functions *----------##

class Users:
    def __init__(self, train_frac, verbose, encrypt):
        # Programm parameters
        self.verbose = verbose
        self.encrypt = encrypt
        self.train_frac = train_frac

        if (self.verbose): print(tc.WARNING+"Initiating the Users [-]"+tc.ENDC)

        self.public_key = u.receiveViaSocket(members.Users, "\t --> Receiving public key from CSP")
        
        if (self.verbose): print(tc.WARNING+"Initiating the Users [-]"+tc.ENDC)

        X, Y, Xtest, Ytest = self.prepareValues(train_frac=self.train_frac)
        # Turn the pandas dataframes into an array
        Xlist = X.values
        Ylist = Y.values

        #initialise the list of (Ai,bi) of all users 
        self.c = []
        # print(len(X))
        bar = ProgressBar(len(X), title="User's contribution encryption")

        for i in range(len(X)):
            x = np.array(Xlist[i])[np.newaxis]
            #be careful, our x is the x.T in the paper
            x = x.T
            y = float(Ylist[i][0])
            a = np.dot(x,x.T)
            b = np.dot(y,x)
            bar.update()
            # append the contribution list, each element of c is [enc(Ai), enc(bi)]
            if (self.encrypt):
                self.c.append([u.encrypt(a, self.public_key), u.encrypt(b, self.public_key)])
            else:
                self.c.append([a,b])
        print('\r')
        if (self.verbose): 
            if (self.encrypt): print(tc.OKGREEN+"\t --> Users have encrypted their contribution with CSP's public key"+tc.ENDC)
            else : print(tc.OKGREEN+"\t --> Users have send (in clair) their contribution with CSP's public key"+tc.ENDC)
        
        u.sendViaSocket(members.Evaluator, self.c, "\t --> Sending list of User's contributions (ai, bi)")

    def prepareValues(self, train_frac=0.8):
        '''
        Function to prepare the values of the dataset before calling the Regression Class
        '''
        # Opening up the dataset using pandas to easily manipulate Dataframe variables
        print(tc.OKGREEN + "Opening up the dataset..."+tc.ENDC)
        file = r'../Datasets/Concrete_Data.xlsx'
        dataset = pd.read_excel(file)
        if(self.verbose): print(dataset.head(5))
        
        # Randomizing the rows of the dataset (separation between training a testing dataset)
        print(tc.OKGREEN + "Shuffling the index of the dataset..."+tc.ENDC)
        dataset = dataset.sample(frac=1).reset_index(drop=True)
        if(self.verbose): print(dataset.head(5))

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

            
Users = Users(train_frac=parameters.train_frac, verbose=parameters.verbose, encrypt=parameters.encrypt)




        

            
       





