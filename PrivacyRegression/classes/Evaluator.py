#!/usr/bin/env python3

'''Ridge Regression test using Python (pandas & numpy)'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "13/11/2018"

import pandas as pd
from phe import paillier
import numpy as np
import math

# Other parties that need to be initiated
import CSP
import Users

from termcol import termcol as tc

##---------* Functions *----------##

class Evaluator:
    def __init__(self, verbose=False):
        # Programm parameters
        self.verbose = verbose

        if (self.verbose):
            print(tc.WARNING+"Initiating the Evaluator..."+tc.ENDC)