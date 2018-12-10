#!/usr/bin/env python3

'''CSP Class for the Privacy Preserving Ridge Regression'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "13/11/2018"

# import pandas as pd
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

class CSP:
    def __init__(self, verbose=False, encrypt=False):
        # Programm parameters
        self.verbose = verbose
        self.encrypt = encrypt

        if (self.verbose): print(tc.WARNING+"Initiating the CSP [-]"+tc.ENDC)

        # Generate the public and private key used for Paillier encryption and decryption
        self.public_key, self.private_key = paillier.generate_paillier_keypair()
        if (self.verbose): print(tc.OKGREEN+"\t --> Key pair generated"+tc.ENDC)
        # Sending public_key to the Users and CSP
        u.sendViaSocket(members.Users, self.public_key, '\t --> Sending public key to Users')
        u.sendViaSocket(members.Evaluator, self.public_key, '\t --> Sending public key to Evaluator')

        
        self.message = u.receiveViaSocket(members.CSP)
        print(self.private_key.decrypt(self.message))

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


CSP = CSP(verbose=True, encrypt=False)