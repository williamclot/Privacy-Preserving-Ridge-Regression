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

##---------* Functions *----------##

class CSP:
    def __init__(self, verbose=False):
        # Programm parameters
        self.verbose = verbose

        if (self.verbose):
            print(tc.WARNING+"Initiating the CSP..."+tc.ENDC)

        # Generate the public and private key used for Paillier encryption and decryption
        self.public_key, self.private_key = paillier.generate_paillier_keypair()
        if (self.verbose):
            print(tc.OKGREEN+"\t --> Key pair generated: OK"+tc.ENDC)


    def decrypt(self, c):
        c_decrypted = []
        for i in len(c):
            c_decrypted.append([self.private_key.decrypt(c[i][0]),self.private_key.decrypt(c[i][1])])


        return c_decrypted








