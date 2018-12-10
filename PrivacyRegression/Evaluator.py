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
import sys
import socket, pickle

# System import classes folder as well
sys.path.insert(0,'./classes/')

from utils import termcol as tc
from utils import utils
from utils import members
u = utils();

##---------* Functions *----------##

class Evaluator:
    def __init__(self, verbose=False, encrypt=False):
        # Programm parameters
        self.verbose = verbose
        if (self.verbose): print(tc.WARNING+"Initiating the Evaluator [-]"+tc.ENDC)

        self.public_key = u.receiveViaSocket(members.Evaluator, "\t --> Receiving public key from CSP")


Evaluator = Evaluator(verbose=True, encrypt=False)