#!/usr/bin/env python3

'''Evaluator Class for the Privacy Preserving Ridge Regression'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "13/11/2018"

import pandas as pd
from phe import paillier
import numpy as np
import math
import random

from termcol import termcol as tc

##---------* Functions *----------##

class Evaluator:
    def __init__(self, public_key, ci_list, lamb, verbose=False):
        # Programm parameters
        self.verbose = verbose
        if (self.verbose): print(tc.WARNING+"Initiating the Evaluator..."+tc.ENDC)
        self.public_key = public_key

        # Contribution list of users encrypted data with CSP's public key
        self.ci_list = ci_list
        if (self.verbose): print(tc.OKGREEN+"Receiving the contributions of the users: OK"+tc.ENDC)

        self.A_enc = ci_list[0][0]
        self.b_enc = ci_list[0][1]

        # Doing the sum of Ai and bi encrypted with paillier homomorphic encryption
        for i in range(1, len(ci_list)):
            self.A_enc += ci_list[i][0]
            self.b_enc += ci_list[i][1]

        # clambda
        clambda = self.encrypt(np.eye(len(self.A_enc))*lamb)
        #self.A_enc += clambda
        self.A_enc = np.dot(self.A_enc,clambda)

        #apply the masks μA and μb on A and b
        Atild, btild = self.random_mask(self.A_enc,self.b_enc)

    def encrypt(self, A):
        '''return c = Cpkcsp(A)'''
        encrypt_func = lambda plain_text: self.public_key.encrypt(plain_text)
        vector_func = np.vectorize(encrypt_func)

    def random_mask(self, A_enc, b_enc):
        '''return E(A+μA), E(b+μb)'''
        mask_add = lambda val: val + self.public_key.encrypt(random.random()*10000)
        vector_func = np.vectorize(mask_add)
        return vector_func(A_enc),vector_func(b_enc)

        