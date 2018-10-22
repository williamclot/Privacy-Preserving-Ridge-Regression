#!/usr/bin/env python3

from phe import paillier
import numpy as np

# Generate the public and private key used for Paillier encryption and decryption
public_key, private_key = paillier.generate_paillier_keypair()

# List of numbers we want to encrypt
secret_number_list = [1, 2, 3]

# We encrypt the list using the public key
encrypted_number_list = [public_key.encrypt(x) for x in secret_number_list]

sum = 0

for i in range(len(encrypted_number_list)) :
    # encrypted_number_list[i] = encrypted_number_list[i] * 2
    sum += encrypted_number_list[i] * 2

# encrypted_mean = np.sum(encrypted_number_list)

print(private_key.decrypt(sum))
