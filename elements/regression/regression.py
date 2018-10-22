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
print(L)


LT = np.transpose(L)
print(LT)

def back_substitution(LT,b):
    d = len(X[0])
    Y = [0]*d

    #last equation of the matrix product
    Y[d-1]=b[d-1]/LT[d-1][d-1]

    for i in range(d-2,-1,-1):
        for j in range(d-1,i,-1):
            b[i]-=LT[i][j]*Y[j]
        Y[i]=b[i]/LT[i][i]

    return Y

#details of operations in back_substitution
# yn=b[7]/LT[7][7]
# print(yn)
# yn1=(b[6]-LT[6][7]*yn)/LT[6][6]
# print(yn1)
# yn2=(b[5]-LT[5][7]*yn-LT[5][6]*yn1)/LT[5][5]
# print(yn2)
# yn3=(b[4]-LT[4][7]*yn-LT[4][6]*yn1-LT[4][5]*yn2)/LT[4][4]
# print(yn3)
# yn4=(b[3]-LT[3][7]*yn-LT[3][6]*yn1-LT[3][5]*yn2-LT[3][4]*yn3)/LT[3][3]
# print(yn4)
# yn5=(b[2]-LT[2][7]*yn-LT[2][6]*yn1-LT[2][5]*yn2-LT[2][4]*yn3-LT[2][3]*yn4)/LT[2][2]
# print(yn5)
# yn6=(b[1]-LT[1][7]*yn-LT[1][6]*yn1-LT[1][5]*yn2-LT[1][4]*yn3-LT[1][3]*yn4-LT[1][2]*yn5)/LT[1][1]
# print(yn6)
# yn7=(b[0]-LT[0][7]*yn-LT[0][6]*yn1-LT[0][5]*yn2-LT[0][4]*yn3-LT[0][3]*yn4-LT[0][2]*yn5-LT[0][1]*yn6)/LT[0][0]
# print(yn7)

Y = back_substitution(LT,b)
print("y=",Y)
beta = back_substitution(L,Y)
print("beta=",beta)
