#!/usr/bin/env python3

'''Users Class for the Privacy Preserving Ridge Regression'''

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
        
        self.c = []


        def encrypt(A,b):

            func = lambda h: self.public_key.encrypt(h)
            vfunc = np.vectorize(func)
            return [vfunc(A),vfunc(b)]

            


        for users in range(len(X)):
            x = np.array(Xlist[users])[np.newaxis]
            x = x.T
            y = float(Ylist[users][0])

            #be careful, our x is the xt in the paper
            a = np.dot(x,x.T)
            b = np.dot(y,x)

            self.c.append(encrypt(a,b))

        
       
        # print(self.Ai)
        # print(self.bi)  
        #self.c.append([[self.public_key.encrypt(xi) for xi in self.Ai],[self.public_key.encrypt(yi) for yi in self.bi]])

            
    



        

            
       





