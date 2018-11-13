#!/usr/bin/env python3

'''Privacy Preserving Ridge Regression'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "13/11/2018"

import pandas as pd
import numpy as np
import math
import sys

# System import classes folder as well
sys.path.insert(0,'./classes/')

import Evaluator
import Users
import CSP

from termcol import termcol as tc

##--------* Global variables *----------##

VERBOSE = True
CSP_Key = ''

##--------* Initiating the actors *---------##

CSP = CSP.CSP(verbose=VERBOSE)
CSP_Key = CSP.public_key #Getting the generated public key

Users = Users.Users(CSP_Key, verbose=VERBOSE)
Evaluator = Evaluator.Evaluator(CSP_Key, verbose=VERBOSE)

