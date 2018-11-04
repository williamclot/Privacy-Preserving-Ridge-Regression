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



def back_substitution_upper(LT,b):
    d = len(b)
    Y = np.zeros((d,1))
    Y[d-1][0]=b[d-1][0]/LT[d-1][d-1]
    for i in range(d-2,-1,-1):
        for j in range(d-1,i,-1):
            b[i][0]=b[i][0]-(LT[i][j]*Y[j][0])
        Y[i][0]=b[i][0]/LT[i][i]

    return Y

def back_substitution_lower(L,Y):
    d = len(Y)
    beta = np.zeros((d,1))
    beta[0][0]=Y[0][0]/L[0][0]
    for i in range(1,d):
        for j in range(0,i):
            Y[i][0]=Y[i][0]-(L[i][j]*beta[j][0])
        beta[i][0]=Y[i][0]/L[i][i]

    return beta

##--------* Regression *---------##

data = opendata("../../datasets/forestfires.csv")

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
print("LT=", LT)
print("L=", L)
print("A=", A)
print("LT*L", np.dot(LT,L))
print("L*LT",np.dot(L,LT))
print(np.array_equal(A,np.dot(L,LT)))
print(np.array_equal([1,2],[1,2]))

# M1up=[[7,0,0,0,0,0,0,0],[1,6,0,0,0,0,0,0],[2,4,5,0,0,0,0,0],[7,3,1,8,0,0,0,0],[6,8,4,2,1,0,0,0],[1,5,8,5,1,2,0,0],[1,1,1,1,1,1,1,0],[2,2,2,2,2,2,2,2]]
# M3up=[[7],[7],[11],[19],[21],[22],[7],[16]]
# M2up=back_substitution_lower(M1up,M3up)
# print("M2up=",M2up)

M1=[[6.3,3.2,2.1],[0,1.7,4.2],[0,0,1.3]]
# M2=[[2,1,3]]
M3=[[22.1],[14.3],[3.9]]
M2=back_substitution_upper(M1,M3)
print("M2=",M2)


#back_substitution to find y
Y = back_substitution_lower(L,b)
print("b=",b)
print("compared to", np.dot(L,Y))

#back_substitution to find beta
beta = back_substitution_upper(LT,Y)
print("Y=",Y)
print("compared to",np.dot(LT,beta))

print("A*beta=",np.dot(A, beta))
print("b=",b)

#print(A)
print(L)
#print(np.dot(L, LT))
