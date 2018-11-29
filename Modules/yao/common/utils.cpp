/*********************************************
Author: William Clot
Email: contact@williamclot.com
Date: 26/11/18
**********************************************/

#include <vector>
#include "utils.h"

using namespace std;

// Simple void function that prints out a vector value to std::cout
void printVector(vector<uint16_t> &vect, int num, string name) {
	cout << name << " vector: \n";
	for (int i = 0; i < num; i++){
		if (i == 0){
			cout << "[";
		}
    	cout << vect[i];
		if (i == num - 1){
			cout << "]\n";
		} else {
			cout << ",";
		}
	}
}

void read_test_options(int32_t* argcp, char*** argvp, e_role* role,
	uint32_t* bitlen, uint32_t* nvals, uint32_t* secparam, std::string* address,
	uint16_t* port, int32_t* test_op, uint32_t* test_bit, std::string* circuit, double* fpa, double* fpb) {

	uint32_t int_port = 0, int_testbit = 0;

	parsing_ctx options[] =
		{ 
			{(void*) &int_testbit, T_NUM, "i", "test bit", false, false },
			{(void*) nvals, T_NUM, "n",	"Number of parallel operation elements", false, false },
			{(void*) bitlen, T_NUM, "b", "Bit-length, default 32", false,false },
			{(void*) secparam, T_NUM, "s", "Symmetric Security Bits, default: 128", false, false },
			{(void*) address, T_STR, "a", "IP-address, default: localhost", false, false },
			{(void*) circuit, T_STR, "c", "circuit file name", false, false },
			{(void*) &int_port, T_NUM, "p", "Port, default: 7766", false, false },
			{(void*) test_op, T_NUM, "t", "Single test (leave out for all operations), default: off", false, false },
			{(void*) fpa, T_DOUBLE, "x", "FP a", false, false },
			{(void*) fpb, T_DOUBLE, "y", "FP b", false, false }
		};

	if (!parse_options(argcp, argvp, options, sizeof(options) / sizeof(parsing_ctx))) {
		print_usage(*argvp[0], options, sizeof(options) / sizeof(parsing_ctx));
		std::cout << "Exiting" << std::endl;
		exit(0);
	}

	if (int_port != 0) {
		assert(int_port < 1 << (sizeof(uint16_t) * 8));
		*port = (uint16_t) int_port;
	}

	*test_bit = int_testbit;
}