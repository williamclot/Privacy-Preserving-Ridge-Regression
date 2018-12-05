import numpy as np
import math as m

A = [[4, 12, -16],[12, 37, -43], [-16, -43, 98]]
A = np.array(A)

# shape[0] --> lignes i
# shape[1] --> colonnes j

def cholesky(A):
    '''Returns cholesky decomposition of A = L * L.T'''
    
    n = A.shape[0]
    L = np.zeros((n, n))

    for i in range(n):
        L[i][i] = m.sqrt(A[i][i] - np.dot(L[i][:],L[i][:]))
        for j in range(i+1, n):
            L[j][i] = (A[j][i] - np.dot(L[i,:], L[j, :]))/L[i][i]
    return L
print(cholesky(A))


########## THINKING OF THE ABY IMPLEMENTATION #########
#-----------------------------------------------------#

# Okay.. Let's rewrite this code as a lower level as possible!

# New input data as form of a list
A = [4, 12, -16, 12, 37, -43, -16, -43, 98]
n = 3
L = [0, 0, 0, 0, 0, 0, 0, 0, 0]

for i in range(n):
    # Calculating the np.dot inside the square root..
    mul = 0
    for k in range(n): mul += L[i*n+k]**2
    # Getting diagonal elements
    L[i*n+i] = (A[i*n+i] - mul) 
    # 
    # for j in range(i+1, n):
    #     mul = 0
    #     for k in range(n): 
    #         mul += L[i*n+k]*L[j*n+k]
    #     # Getting the [j][i] element
    #     L[j*n+i] = (A[j*n+i]-mul)/L[i*n+i]
print(L)



