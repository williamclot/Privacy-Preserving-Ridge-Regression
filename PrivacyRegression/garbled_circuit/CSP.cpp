#include <ENCRYPTO_utils/crypto/crypto.h>
#include <ENCRYPTO_utils/parse_options.h>
#include <abycore/aby/abyparty.h>
#include <abycore/circuit/share.h>
#include <abycore/circuit/booleancircuits.h>
#include <abycore/sharing/sharing.h>
#include <cassert>
#include <iomanip>
#include <iostream>
#include <math.h>

// My Libraries
#include "common/circuit.h"
#include "common/utils.h"

int main(int argc, char** argv) {

	// std::cout << "Launching CSP [-]" << std::endl;

	// Hardcoded server role
	e_role role = SERVER;
	uint32_t nvals = 25, secparam = 128, nthreads = 1;

	uint16_t port = 7766;
	std::string address = "127.0.0.1";
	std::string input_file = "";
	std::string circuit = "none.aby";
	int32_t test_op = -1;
	e_mt_gen_alg mt_alg = MT_OT;
	uint32_t test_bit = 0;

	// Reading options
	read_test_options(&argc, &argv, &role, &nvals, &secparam, &address,
		&port, &test_op, &input_file, &circuit);

	// Reading the inputs in the /input folder and parsing them in a std::vector
	std::vector<double> Amask;
	std::vector<double> bmask;
	
	Amask = get_input("inputs/Amask");
	bmask = get_input("inputs/bmask");
	
	int n = sqrt(nvals);

	// print_vector(Amask, nvals, "Opening CSP data (Amask)...");
	// print_vector(bmask, n, "Opening CSP data (bmask)...");

	seclvl seclvl = get_sec_lvl(secparam);

	test_circuit(role, address, port, seclvl, nvals, nthreads, mt_alg, S_BOOL, Amask, bmask);

	return 0;
}
