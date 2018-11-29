/*********************************************
Author: William Clot
Email: contact@williamclot.com
Date: 26/11/18
**********************************************/

#ifndef _UTILS_
#define _UTILS_

#include <stdint.h>
#include <iostream>
#include <ENCRYPTO_utils/crypto/crypto.h>
#include <ENCRYPTO_utils/parse_options.h>
#include <abycore/aby/abyparty.h>
#include <abycore/circuit/share.h>
#include <abycore/circuit/booleancircuits.h>
#include <abycore/sharing/sharing.h>
#include <cassert>
#include <iomanip>
#include <iostream>

using namespace std;

// Function that enables to print a Vector to std::cout
void printVector(vector<uint16_t> &vect, int num, string name);

// Function to read options and inputs
void read_test_options(int32_t* argcp, char*** argvp, e_role* role,
	uint32_t* bitlen, uint32_t* nvals, uint32_t* secparam, std::string* address,
	uint16_t* port, int32_t* test_op, uint32_t* test_bit, std::string* circuit, double* fpa, double* fpb);

#endif