
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

import Evalutator
import Users
import CSP

from termcol import termcol as tc

##--------* Global 

##--------* Initiating the actors *---------##

Evalutator = Evalutator.Evalutator(verbose)
Users = Users.Users(verbose)
CSP = CSP.CSP(verbose)