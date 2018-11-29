#include <ENCRYPTO_utils/crypto/crypto.h>
#include <ENCRYPTO_utils/parse_options.h>
#include <abycore/aby/abyparty.h>
#include <abycore/circuit/share.h>
#include <abycore/circuit/booleancircuits.h>
#include <abycore/sharing/sharing.h>
#include <cassert>
#include <iomanip>
#include <iostream>

// My Libraries
#include "common/circuit.h"
#include "common/utils.h"

int main(int argc, char** argv) {
	
	// Hardcoded client role
	e_role role = CLIENT;
	uint32_t bitlen = 1, nvals = 4, secparam = 128, nthreads = 1;

	uint16_t port = 7766;
	std::string address = "127.0.0.1";
	std::string circuit = "none.aby";
	int32_t test_op = -1;
	e_mt_gen_alg mt_alg = MT_OT;
	uint32_t test_bit = 0;
	double fpa = 0, fpb = 0;

	// Reading options
	read_test_options(&argc, &argv, &role, &bitlen, &nvals, &secparam, &address,
		&port, &test_op, &test_bit, &circuit, &fpa, &fpb);

	seclvl seclvl = get_sec_lvl(secparam);


	test_circuit(role, address, port, seclvl, nvals, nthreads, mt_alg, S_BOOL, fpa, fpb);

	return 0;
}
