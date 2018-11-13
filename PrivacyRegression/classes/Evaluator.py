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

        self.ci_list = ci_list
        if (self.verbose): print(tc.GREENOK+"Receiving the contributions of the users: OK"+tc.ENDC)



        