
import pandas as pd
import numpy as np
import math

import Regression

##--------* Regression *---------##

Regression = Regression.Regression("../../datasets/forestfires.csv")

# data = rd.opendata("../../datasets/forestfires.csv")

# computing A
A, Xt = Regression.getA(Regression.X)

# computing b
b = Regression.getb(Xt, Regression.Y)

# spliting A into L and LT
L = Regression.cholesky0(A)
LT = np.transpose(L)

#back_substitution to find y
Y = Regression.back_substitution_lower(L,b)
print("b=",b)
print("compared to", np.dot(L,Y))

#back_substitution to find beta
beta = Regression.back_substitution_upper(LT,Y)
print("Y=",Y)
print("compared to",np.dot(LT,beta))

# checking the equation A*beta=b
print("A*beta=",np.dot(A, beta))
print("b=",b)
print("beta=",beta)


# checking the result when dealing with small data set by inversing the matrix A
Ainv=np.linalg.inv(A)
print(np.dot(Ainv,b))