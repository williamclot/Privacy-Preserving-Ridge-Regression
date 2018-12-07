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
from progressbar import ProgressBar

##---------* Functions *----------##

class Users:
    def __init__(self, public_key, X, Y, verbose=False, encrypt=True):
        # Programm parameters
        self.verbose = verbose
        self.public_key = public_key

        if (self.verbose):
            print(tc.WARNING+"Initiating the Users..."+tc.ENDC)

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
            if (encrypt):
                self.c.append(self.encrypt(a,b))
            else:
                self.c.append([a,b])
        print('\r')
        if (self.verbose): 
            if (encrypt): print(tc.OKGREEN+"\t --> Users have encrypted their contribution with CSP's public key : OK"+tc.ENDC)
            else : print(tc.OKGREEN+"\t --> Users have send (in clair) their contribution with CSP's public key : OK"+tc.ENDC)


    def encrypt(self, A, b):
        '''return c = Cpkcsp(A, b)'''
        encrypt_func = lambda plain_text: self.public_key.encrypt(plain_text)
        vector_func = np.vectorize(encrypt_func)

        return [vector_func(A), vector_func(b)]

            
    



        

            
       





