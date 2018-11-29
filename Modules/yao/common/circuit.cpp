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
	e_mt_gen_alg mt_alg, e_sharing sharing, std::vector <double> data) {

	// we operate on doubles, so set bitlen to 64 bits
	uint32_t bitlen = 64;

	ABYParty* party = new ABYParty(role, address, port, seclvl, bitlen, nthreads, mt_alg);

	std::vector<Sharing*>& sharings = party->GetSharings();

	BooleanCircuit* circ = (BooleanCircuit*) sharings[sharing]->GetCircuitBuildRoutine();

	// print_vector(data, nvals, "Opening CSP data...");


	// // point a uint64_t pointer to the two input floats without casting the content
	// uint64_t *aptr = (uint64_t*) &afp;
	// uint64_t *bptr = (uint64_t*) &bfp;

	// // array of 64 bit values
	// uint64_t avals[nvals];
	// uint64_t bvals[nvals];

	// // fill array with input values nvals times.
	// std::fill(avals, avals + nvals, *aptr);
	// std::fill(bvals, bvals + nvals, *bptr);

	// // SIMD input gates
	// share* ain = circ->PutSIMDINGate(nvals, avals, bitlen, SERVER);
	// share* bin = circ->PutSIMDINGate(nvals, bvals, bitlen, CLIENT);

	// // FP addition gate
	// share* sum = circ->PutFPGate(ain, bin, ADD, nvals, no_status);

	// // output gate
	// share* res_out = circ->PutOUTGate(sum, ALL);

	// // run SMPC
	// party->ExecCircuit();

	// // retrieve plain text output
	// uint32_t out_bitlen, out_nvals;
	// uint64_t *out_vals;
	// res_out->get_clear_value_vec(&out_vals, &out_bitlen, &out_nvals);

	// // print every output
	// for (uint32_t i = 0; i < nvals; i++) {

	// 	// dereference output value as double without casting the content
	// 	double val = *((double*) &out_vals[i]);

	// 	std::cout << "RES: " << val << std::endl;
	// }
}