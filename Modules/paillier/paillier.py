#!/usr/bin/env python3

from phe import paillier
import numpy as np

# Generate the public and private key used for Paillier encryption and decryption
public_key, private_key = paillier.generate_paillier_keypair()

# List of numbers we want to encrypt
secret_number_list = [3, 5, 7, 9, 11]

# We encrypt the list using the public key
encrypted_number_list = [public_key.encrypt(x) for x in secret_number_list]


def sum_mult(encrypted_number_list, private_key):
    sum = 0
    for i in range(len(encrypted_number_list)) :
        # encrypted_number_list[i] = encrypted_number_list[i] * 2
        sum += encrypted_number_list[i] * 2
    # encrypted_mean = np.sum(encrypted_number_list)

    return private_key.decrypt(sum)


def mean(encrypted_number_list, private_key):
    sum = 0
    for i in range(len(encrypted_number_list)):
        sum += encrypted_number_list[i]
    mean = sum / len(encrypted_number_list)
    return private_key.decrypt(mean)




print("sum of element multiplied by 2 =", sum_mult(encrypted_number_list, private_key))
print("mean of the list is =", mean(encrypted_number_list, private_key))
