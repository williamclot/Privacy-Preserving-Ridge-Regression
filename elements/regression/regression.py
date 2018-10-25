#!/usr/bin/env python3

""""Ridge Regression test using Python (pandas & numpy)"""

__author__ = "William CLOT, williamclot.github.com"
__license__ = "MIT"
__date__ = "22/10/2018"

import pandas as pd
import numpy as np
import math

##---------* Functions *----------##

def opendata(url):
    return pd.read_csv(url)

def getA(X, lamb=0.1):
    '''get A from X and lambda'''
    d = len(X[0])
    I = np.eye(d)
    Xt = np.transpose(X)

    A = np.dot(Xt, X)+lamb*I

    return A, Xt

def getb(Xt, Y):
    '''get b from Xt and Y'''
    b = np.dot(Xt, Y)

    return b


def cholesky0(A):
    """
       Performs a Cholesky decomposition of on symmetric, pos-def A.
       Returns lower-triangular L (full sized, zeroed above diag)
    """
    n = A.shape[0]
    L = np.zeros_like(A)

    # Perform the Cholesky decomposition
    for row in range(n):
        for col in range(row+1):
            tmp_sum = np.dot(L[row,:col], L[col,:col])
            if (row == col): # Diagonal elements
                L[row, col] = math.sqrt(max(A[row,row] - tmp_sum, 0))
            else:
                L[row,col] = (1.0 / L[col,col]) * (A[row,col] - tmp_sum)
    return L
#perform a back substitution to find y first and then beta
def back_substitution(LT,b):
    d = len(X[0])
    Y = np.zeros((d,1))
    
    #last equation of the matrix product
    Y[d-1][0]=b[d-1][0]/LT[d-1][d-1]

    for i in range(d-2,-1,-1):
        for j in range(d-1,i,-1):
            b[i][0]=b[i][0]-(LT[i][j]*Y[j])
        Y[i][0]=b[i][0]/LT[i][i]

    return Y

##--------* Regression *---------##

data = opendata("./../../datasets/forestfires.csv")

Y = data[['area']].values

# Applying the logarithm model to the area
for i in range(len(Y)):
    Y[i] = math.log(Y[i]+1)

X = data[['FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain']].values

A, Xt = getA(X)
b = getb(Xt, Y)
L = cholesky0(A)
LT = np.transpose(L)


#back_substitution to find y
Y = back_substitution(LT,b)

#back_substitution to find beta
beta = back_substitution(L,Y)
print("beta =\n",beta)
