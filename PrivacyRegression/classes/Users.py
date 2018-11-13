#!/usr/bin/env python3

'''Ridge Regression test using Python (pandas & numpy)'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "13/11/2018"

import pandas as pd
from phe import paillier
import numpy as np
import math

from termcol import termcol as tc

##---------* Functions *----------##

class Users:
    def __init__(self, public_key, X, Y, verbose=False):
        # Programm parameters
        self.verbose = verbose
        self.public_key = public_key

        if (self.verbose):
            print(tc.WARNING+"Initiating the Users..."+tc.ENDC)


        # turn the database into an array
        Xlist = X.values
        Ylist = Y.values

        #initialise the list of (Ai,bi) of all users 
        self.Ai = []
        self.bi = []
        self.c = []

        for users in range(len(X)):
            x = list(Xlist[users])
            print(x)
            xt = np.transpose(x)
            print(xt)
            y = Ylist[users]
            #self.Ai.append(np.dot(x,xt))
            # print(self.Ai)
            #self.bi.append(np.dot(y,x))
            # print(self.bi)
        # print(self.Ai)
        # print(self.bi)  
        #self.c.append([[self.public_key.encrypt(xi) for xi in self.Ai],[self.public_key.encrypt(yi) for yi in self.bi]])

            
    



        

            
       





