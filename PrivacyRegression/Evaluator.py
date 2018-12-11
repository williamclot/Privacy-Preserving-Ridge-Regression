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
import sys, os, subprocess
import socket, pickle

# System import classes folder as well
sys.path.insert(0,'./classes/')

from utils import termcol as tc
from utils import utils
from utils import members
from utils import parameters 
u = utils();

##---------* Functions *----------##

class Evaluator:
    def __init__(self, lamb, verbose, encrypt):
        # Programm parameters
        self.verbose = verbose
        self.encrypt = encrypt
        self.lamb = lamb

        if (self.verbose): print(tc.WARNING+"Initiating the Evaluator [-]"+tc.ENDC)

        self.public_key = u.receiveViaSocket(members.Evaluator, "\t --> Receiving public key from CSP")
        
        ci_list = u.receiveViaSocket(members.Evaluator, "\t --> Receiving list of User's contributions (ai, bi)")

        self.A_enc = ci_list[0][0]
        self.b_enc = ci_list[0][1]

        # Doing the sum of Ai and bi encrypted with paillier homomorphic encryption
        if (self.verbose): print(tc.OKGREEN+"\t --> Summing ai, bi to get A and b"+tc.ENDC)
        for i in range(1, len(ci_list)):
            self.A_enc += ci_list[i][0]
            self.b_enc += ci_list[i][1]

        # clambda
        if(self.encrypt):
            clambda = u.encrypt(np.eye(len(self.A_enc))*self.lamb, self.public_key)
        else:
            clambda = np.eye(len(self.A_enc))*self.lamb

        # Adding the lamb identity matrix
        self.A_enc += clambda

        #apply the masks μA and μb on A and b
        if (self.verbose): print(tc.OKGREEN+"\t --> Generating muA and mub"+tc.ENDC)
        self.muA , self.mub = self.getMu(self.A_enc), self.getMu(self.b_enc)
        if (self.verbose): print(tc.OKGREEN+"\t --> Adding muA and mub to A and b"+tc.ENDC)
        self.Amask , self.bmask = self.A_enc + self.muA , self.b_enc + self.mub

        size = len(self.Amask)

        u.sendViaSocket(members.CSP, [self.Amask, self.bmask], '\t --> Sending Amask and bmask to CSP')

        if (self.verbose): print(tc.OKGREEN+"\t --> Preparing muA and mub to be put as input in garbled circuit"+tc.ENDC)
        u.ParseToFile(self.muA, "inputs/muA")
        u.ParseToFile(self.mub, "inputs/mub")

        if (self.verbose): print(tc.WARNING+"Initiating Circuit [-]"+tc.ENDC)
        if (self.verbose): print(tc.HEADER+"\t --> Circuit calculations..."+tc.ENDC)

        args = ("./garbled_circuit/build/Evaluator_Circuit", "-n", str(size**2) , "-a", members.CSP['ip'])
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()
        output = output.decode("utf-8")
        beta = output.split("\n")[:-1]
        beta = list(map(float, beta))
        print(beta)

    def getMu(self, matrix):
        '''return μA or μb (mask)'''
        mu = np.zeros((len(matrix),len(matrix[0])))
        reference_power = len(str(int(matrix[0][0])))
        add_rand = lambda val: val + random.random()*10**(reference_power-1)
        vector_func = np.vectorize(add_rand)
        return vector_func(mu)

Evaluator = Evaluator(lamb=parameters.lamb, verbose=parameters.verbose, encrypt=parameters.encrypt)