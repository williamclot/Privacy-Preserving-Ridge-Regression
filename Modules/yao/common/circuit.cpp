#include "circuit.h"
#include <ENCRYPTO_utils/crypto/crypto.h>
#include <ENCRYPTO_utils/parse_options.h>
#include <abycore/circuit/booleancircuits.h>
#include <abycore/circuit/arithmeticcircuits.h>
#include <abycore/circuit/circuit.h>
#include <abycore/circuit/share.h>
#include <abycore/sharing/sharing.h>
#include <abycore/aby/abyparty.h>
#include <math.h>
#include <cassert>
#include <iomanip>
#include <iostream>
#include "utils.h"

void test_circuit(e_role role, const std::string& address, uint16_t port, seclvl seclvl, uint32_t nvals, uint32_t nthreads,
	e_mt_gen_alg mt_alg, e_sharing sharing, std::vector<double> data) {

	// we operate on doubles, so set bitlen to 64 bits
	uint32_t bitlen = 64;

	ABYParty* party = new ABYParty(role, address, port, seclvl, bitlen, nthreads, mt_alg);

	std::vector<Sharing*>& sharings = party->GetSharings();

	BooleanCircuit* circ = (BooleanCircuit*) sharings[sharing]->GetCircuitBuildRoutine();

	// Converting double values to vector of uint64 pointers to double value...

	uint64_t input_csp[nvals];
	uint64_t input_eval[nvals];

	for(int i = 0; i < nvals; i++){
		double value = data[i];
		uint64_t *valuetr = (uint64_t*) &value;
		input_csp[i] = *valuetr;
		input_eval[i] = *valuetr;
	}

	// SIMD input gates
	share* csp_in = circ->PutSIMDINGate(nvals, input_csp, bitlen, SERVER);
	share* eval_in = circ->PutSIMDINGate(nvals, input_eval, bitlen, CLIENT);

	// // FP addition gate
	share* sum = circ->PutFPGate(csp_in, eval_in, SUB, nvals, no_status);

	// // output gate
	share* res_out = circ->PutOUTGate(sum, ALL);

	// // run SMPC
	party->ExecCircuit();

	// // retrieve plain text output
	uint32_t out_bitlen, out_nvals;
	uint64_t *out_vals;
	res_out->get_clear_value_vec(&out_vals, &out_bitlen, &out_nvals);

	if (role == CLIENT) {
		// print every output
		for (uint32_t i = 0; i < nvals; i++) {

			// dereference output value as double without casting the content
			double val = *((double*) &out_vals[i]);

			std::cout << val << std::endl;
		}
	}

}