#!/usr/bin/env python3

'''Evaluator Class for the Privacy Preserving Ridge Regression'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "13/11/2018"

import pandas as pd
from phe import paillier
import numpy as np
import math

from termcol import termcol as tc

##---------* Functions *----------##

class Evaluator:
    def __init__(self, public_key, ci_list, verbose=False):
        # Programm parameters
        self.verbose = verbose
        if (self.verbose): print(tc.WARNING+"Initiating the Evaluator..."+tc.ENDC)

        # Contribution list of users encrypted data with CSP's public key
        self.ci_list = ci_list
        if (self.verbose): print(tc.GREENOK+"Receiving the contributions of the users: OK"+tc.ENDC)

        self.A_enc = np.zeros((len(ci_list), len(ci_list)))
        self.b_enc = np.zeros((len(ci), 1))

        # Doing the sum of Ai and bi encrypted with paillier homomorphic encryption
        for i in range(len(ci_list)):
            self.A_enc += ci_list[i][0]
            self.b_enc += ci_list[i][1]

    def encrypt(self, A, b):
        '''return c = Cpkcsp(A, b)'''
        encrypt_func = lambda plain_text: self.public_key.encrypt(plain_text)
        vector_func = np.vectorize(encrypt_func)

        return [vector_func(A), vector_func(b)]

        