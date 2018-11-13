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



        X = X.values
        print(X)
        Y = Y.values
        # for   
        #     X[i][j]*X
       





