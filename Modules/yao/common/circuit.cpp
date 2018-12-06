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

	BooleanCircuit* bc = (BooleanCircuit*) sharings[S_BOOL]->GetCircuitBuildRoutine();
	ArithmeticCircuit* ac = (ArithmeticCircuit*) sharings[S_ARITH]->GetCircuitBuildRoutine();
	Circuit* yc = (Circuit*) sharings[S_YAO]->GetCircuitBuildRoutine();

	// DATA FORMATTING
	// -----------------------------------

	uint64_t input_csp[nvals];
	uint64_t input_eval[nvals];

	for(int i = 0; i < nvals; i++){
		double value = data[i];
		uint64_t *valuetr = (uint64_t*) &value;
		input_csp[i] = *valuetr;
		input_eval[i] = *valuetr;
	}

	// Putting a vector of zeros to initiate Lower decomposition of cholesky
	uint64_t zeros[nvals] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
	uint64_t zero = 0;

	// Using 0.5 for the sqrt approximation
	double halffp = 0.5;
	uint64_t *valuetr = (uint64_t*) &halffp;
	uint64_t input_half = *valuetr;

	// CIRCUIT INPUTS
	// -----------------------------------

	// SIMD input gates
	share* csp_in = bc->PutSIMDINGate(nvals, input_csp, bitlen, SERVER); // A + mu_a
	share* eval_in = bc->PutSIMDINGate(nvals, input_eval, bitlen, CLIENT); // mu_a

	// Reference inputs (0.5, 0, {0, 0,... , 0})
	share* L = ac->PutSIMDINGate(nvals, zeros, bitlen, SERVER); // zeros
	share* zero_share = bc->PutINGate(zero, bitlen, SERVER);
	share* half = bc->PutINGate(input_half, bitlen, SERVER);

	// CIRCUIT OPERATIONS
	// -----------------------------------

	// FP substraction gate to remove mask mu_A from A + mu_a
	share* A = MatrixSubstraction(csp_in, eval_in, bc, nvals);
	L = Cholesky(A, L, zero_share, half, bitlen, nvals, ac, bc, yc);
	
	uint32_t n = sqrt(nvals);
	share* LT = transpose(L, n, ac, bc, yc);

	// CIRCUIT OUTPUTS
	// -----------------------------------


	share* res_out = ac->PutOUTGate(LT, ALL);

	// run SMPC
	party->ExecCircuit();

	// retrieve plain text output
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

share* MatrixSubstraction(share *s_A, share *s_B, BooleanCircuit *bc, uint32_t nvals){
	/*~~~~ returns a share with a two by two substration between s_A and s_B ~~~~~*/

	/*  Initial states of sharings.
		s_A -> BOOL
		s_B -> BOOL
	*/

	share* out = bc->PutFPGate(s_A, s_B, SUB, nvals, no_status); // s_A and s_B are in Boolean share
	return out;
}

share* ExtractIndex(share *s_x , uint32_t i, uint32_t bitlen, ArithmeticCircuit *ac, BooleanCircuit *bc, Circuit *yc){
	/*~~~~ returns a share of the ith wire of s_x ~~~~~*/

	/*  Initial states of sharings.
		s_x -> ARITHM
		out -> BOOL
	*/

	uint64_t zero = 0;
	share* out = ac->PutCONSGate(zero,bitlen);

	out->set_wire_id(0, s_x->get_wire_id(i));
	
	out = bc->PutY2BGate(yc->PutA2YGate(out)); //Converting to bc

	return out;
}

share* SqurtApprox(share *element, share *half, uint32_t step, ArithmeticCircuit *ac, BooleanCircuit *bc, Circuit *yc){
	/*~~~~ returns a share with an Babylonian approximation of a square root of element ~~~~~*/

	/*  Initial states of sharings.
		element -> BOOL
		half -> BOOL
	*/

	share* temp = element;
	share* division;

	for(int i=0; i<step; i++){
		division = bc->PutFPGate(element, temp, DIV);
		division = bc->PutFPGate(temp, division, ADD);
		temp = bc->PutFPGate(half, division, MUL);
	}

	return temp;
}

share* Cholesky(share *A, share *L, share *zero_share, share *half, uint32_t bitlen, uint32_t nvals, ArithmeticCircuit *ac, BooleanCircuit *bc, Circuit *yc){
	/*~~~~ returns a share with the Cholesky decomposition of A ~~~~~*/

	/*Initial states of sharings.
		A -> BOOL
		L -> ARITH
		zero_share -> ARITH
	*/

	int n = sqrt(nvals); // number of lines (OK)
	uint32_t index; // int to access particular indexes of SIMD gates

	A = ac->PutB2AGate(A);
	A = ac->PutSplitterGate(A);
	L = ac->PutSplitterGate(L);

	for(int i=0; i<n; i++){
		
		share* mul = zero_share;
		share* temp;
		share* tempi;
		share* currentL;

		for(int k=0; k<n; k++){
			index = i*n+k;
			temp = ExtractIndex(L, index, bitlen, ac, bc, yc); // L[i*n+k]
			temp = bc->PutFPGate(temp, temp, MUL, no_status); // currentL**2
			mul = bc->PutFPGate(mul, temp, ADD, no_status); // mul += currentL**2
		}
		
		index=i*n+i;
		temp = ExtractIndex(A, index, bitlen, ac, bc, yc); // A[i*(n+1)]
		temp = bc->PutFPGate(temp, mul, SUB, no_status); // L[i*n+i] = (A[i*n+i] - mul) 

		temp = SqurtApprox(temp, half, 5, ac, bc, yc);
		currentL = temp; // Nice little optimization to avoid extracting this value later on from L
		temp = ac->PutB2AGate(temp); // convert L[i*n+i] from bc to ac
		L->set_wire_id(index, temp->get_wire_id(0)); // append the new values to L.

		for (int j=i+1; j<n; j++){
			mul = zero_share;
			for (int k=0; k < n; k++){
				index = i*n+k;
				temp = ExtractIndex(L, index, bitlen, ac, bc, yc); // extract L[i*n+k] from L
				index = j*n+k;
				tempi = ExtractIndex(L, index, bitlen, ac, bc, yc); // extract L[j*n+k] from L
				temp = bc->PutFPGate(temp, tempi, MUL, no_status); // compute L[i*n+k]*L[j*n+k]
				mul = bc->PutFPGate(mul, temp, ADD, no_status); // mul += L[i*n+k]*L[j*n+k]
			}
			index = j*n+i;
			temp = ExtractIndex(A, index, bitlen, ac, bc, yc); // A[j*n+i]
			temp = bc->PutFPGate(temp, mul, SUB, no_status); // A[j*n+i]-mul
			index = i*n+i;
			temp = bc->PutFPGate(temp, currentL, DIV, no_status);
			temp = ac->PutB2AGate(temp); // convert bc to ac
			index = j*n+i;
			L->set_wire_id(index, temp->get_wire_id(0)); // append the new values to L.
		}
	}
	L = ac->PutCombinerGate(L);
	return L;
}

share* transpose(share *L, uint32_t n, ArithmeticCircuit *ac, BooleanCircuit *bc, Circuit *yc){

	/*Initial states of sharings.
		L -> ARITH and combined
	*/

	share* temp = L;
	uint32_t index1;
	uint32_t index2;
	temp = ac->PutSplitterGate(temp);
	L = ac->PutSplitterGate(L);
	for (int i = 0; i < n; i++){
		for (int j=0; j<n; j++){
			index1 = i*n+j;
			index2 = j*n+i;
			temp->set_wire_id(index1, L->get_wire_id(index2)); 
		}
	}
	temp = ac->PutCombinerGate(temp);
	return temp;
}
