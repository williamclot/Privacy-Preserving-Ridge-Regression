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
void print_vector(vector<double> &vect, int num, string name);

// Function to read options and inputs
void read_test_options(int32_t* argcp, char*** argvp, e_role* role,
	uint32_t* nvals, uint32_t* secparam, std::string* address,
	uint16_t* port, int32_t* test_op, std::string* input_file, std::string* circuit);

// Getting the input from a file
std::vector<double> get_input(std::string file_name);

#endif