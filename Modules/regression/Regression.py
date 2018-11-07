#!/usr/bin/env python3

'''Ridge Regression test using Python (pandas & numpy)'''

__author__ = "William CLOT, www.github.com/williamclot; Camille PLAYS, www.github.com/camilleplays"
__license__ = "MIT"
__date__ = "22/10/2018"

import pandas as pd
import numpy as np
import math

##---------* Functions *----------##

class Regression:
    def __init__(self, X, Y, lamb=0.1):
        # Input X, Output Y
        self.Ymin, self.Ymax, self.Y = self.uniform(Y)
        self.Xmin, self.Xmax, self.X = self.uniform(X)

        self.lamb = lamb

        # Result beta of Regression
        self.beta = []

    def train_model(self):
        '''
        Trains model using the training dataset
        '''
        # A and b from X and Y
        A, Xt = self.getA(self.X, self.lamb)
        b = np.dot(Xt, self.Y)

        # Cholesky Decomposition
        L, Lt = self.cholesky0(A)

        self.beta = self.back_substitution_upper(Lt, self.back_substitution_lower(L, b))


    def test_model(self, Xtest, Ytest):
        '''
        Testing the model with the last 0.2 of the dataset left, uniforming the values with the same max and min used to train the model (questions to ask)
        '''
        #Uniformizing the inputs on the same range as the training data
        for column in Xtest:
            Xtest[column]=(Xtest[column]-self.Xmin[column])/(self.Xmax[column]-self.Xmin[column])
        for column in Ytest:
            Ytest[column]=(Ytest[column]-self.Ymin[column])/(self.Ymax[column]-self.Ymin[column])

        # back to arrays from pandas dataframe
        Xtest = Xtest.values
        Ytest = Ytest.values

        # compute transpose of beta
        tbeta = np.transpose(self.beta)

        # loop over each contribution, compute performance of our model
        sum_err = 0
        for i in range(len(Xtest)):
            predictedY = np.dot(tbeta, Xtest[i])
            sum_err += float(abs(Ytest[i] - float(predictedY)))

        sum_err = sum_err/Xtest.shape[0]
        return sum_err*self.Ymax[0]


    def uniform(self, frame):
        '''
        Uniformizing dataset on [0, 1] range depending on min and max values of each column
        '''
        # max and min values for each column (returns a dataframe)
        maxV = frame.max()
        minV = frame.min()

        for column in frame:
            frame[column]=(frame[column]-minV[column])/(maxV[column]-minV[column])
        
        return minV, maxV, frame.values

    def getA(self, X, lamb):
        '''
        Get A from X and lambda
        '''
        d = len(X[0])
        I = np.eye(d)
        Xt = np.transpose(X)

        A = np.dot(Xt, X)+lamb*I

        return A, Xt

    def cholesky0(self, A):
        '''
        Performs a Cholesky decomposition of on symmetric, pos-def A.
        Returns lower-triangular L (full sized, zeroed above diag)
        '''
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
        return L, np.transpose(L)

    def back_substitution_upper(self, LT, Y):
        tmp = np.copy(Y)
        d = len(tmp)
        Y = np.zeros((d,1))
        Y[d-1][0]=tmp[d-1][0]/LT[d-1][d-1]
        for i in range(d-2,-1,-1):
            for j in range(d-1,i,-1):
                tmp[i][0]=tmp[i][0]-(LT[i][j]*Y[j][0])
            Y[i][0]=tmp[i][0]/LT[i][i]

        return Y

    def back_substitution_lower(self, L, b):
        tmp = np.copy(b)
        d = len(tmp)
        beta = np.zeros((d,1))
        beta[0][0]=tmp[0][0]/L[0][0]
        for i in range(1,d):
            for j in range(0,i):
                tmp[i][0]=tmp[i][0]-(L[i][j]*beta[j][0])
            beta[i][0]=tmp[i][0]/L[i][i]

        return beta



