#!/usr/bin/env python3

'''CSP Class for the Privacy Preserving Ridge Regression'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "13/11/2018"

import pandas as pd
from phe import paillier
import numpy as np
import math

from termcol import termcol as tc
from termcol import utils as utils

import subprocess
import sys

##---------* Functions *----------##

class CSP:
    def __init__(self, verbose=False, encrypt=False):
        # Programm parameters
        self.verbose = verbose
        self.encrypt = encrypt

        if (self.verbose): print(tc.WARNING+"Initiating the CSP..."+tc.ENDC)

        # Generate the public and private key used for Paillier encryption and decryption
        self.public_key, self.private_key = paillier.generate_paillier_keypair()
        if (self.verbose): print(tc.OKGREEN+"\t --> Key pair generated: OK"+tc.ENDC)

        self.Amask = 0
        self.bmask = 0


    def decrypt(self, A):
        decrypt_func = lambda cipher_text: self.private_key.decrypt(cipher_text)
        vector_func = np.vectorize(decrypt_func)

        return vector_func(A)

    def receiveEvaluator(self, Amask, bmask):
        if(self.encrypt):
            self.Amask = self.decrypt(Amask)
            self.bmask = self.decrypt(bmask)
        else:
            self.Amask = Amask
            self.bmask = bmask
        
        utils.ParseToFile(self.Amask, "garbled_circuit/inputs/Amask")
        utils.ParseToFile(self.bmask, "garbled_circuit/inputs/bmask")

        # subprocess.call("./garbled_circuit/build/CSP")


