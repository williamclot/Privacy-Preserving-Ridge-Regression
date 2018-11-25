#include "matrix_sub.h"
#include <abycore/sharing/sharing.h>

int32_t test_matrix_sub_circuit(e_role role, const std::string& address, uint16_t port, seclvl seclvl,
		uint32_t nvals, uint32_t bitlen, uint32_t nthreads, e_mt_gen_alg mt_alg,
		e_sharing sharing, uint32_t num) {

	/**
	 Step 1: Create the ABYParty object which defines the basis of all the
	 operations which are happening.	Operations performed are on the
	 basis of the role played by this object.
	 */
	ABYParty* party = new ABYParty(role, address, port, seclvl, bitlen, nthreads,
			mt_alg);

	/**
	 Step 2: Get to know all the sharing types available in the program.
	 */
	std::vector<Sharing*>& sharings = party->GetSharings();

	/**
	 Step 3: Create the circuit object on the basis of the sharing type
	 being inputed.
	 */
	ArithmeticCircuit* circ =
			(ArithmeticCircuit*) sharings[sharing]->GetCircuitBuildRoutine();

	/**
	 Step 4: Creating the share objects - s_x_vec, s_y_vec which
	 are used as inputs to the computation. Also, s_out which stores the output.
	 */

	share *s_x_vec, *s_y_vec, *s_out;

	/**
	 Step 5: Allocate the xvals and yvals that will hold the plaintext values.
	 */
	uint16_t x, y;

	uint32_t out_bitlen , out_nvals , *out_vals;

	std::vector<uint16_t> xvals(num);
	std::vector<uint16_t> yvals(num);

	uint32_t i;
	
	/**
	 Step 6: Fill the arrays xvals and yvals with the generated random values.
	 Both parties use the same seed, to be able to verify the
	 result. In a real example each party would only supply
	 one input value. Copy the randomly generated vector values into the respective
	 share objects using the circuit object method PutINGate().
	 Also mention who is sharing the object.
	 The values for the party different from role is ignored,
	 but PutINGate() must always be called for both roles.
	 */
	for (i = 0; i < num; i++) {

		x = i+5;
		y = i;

		xvals[i] = x;
		yvals[i] = y;
	}

	s_x_vec = circ->PutSIMDINGate(num, xvals.data(), 16, SERVER);
	s_y_vec = circ->PutSIMDINGate(num, yvals.data(), 16, CLIENT);

	/**
	 Step 7: Call the build method for building the circuit for the
	 problem by passing the shared objects and circuit object.
	 Don't forget to type cast the circuit object to type of share
	 */
	s_out = BuildMatrixSubCircuit(s_x_vec, s_y_vec, num,
			(ArithmeticCircuit*) circ);

	/**
	 Step 8: Output the value of s_out (the computation result) to both parties
	 */
	s_out = circ->PutOUTGate(s_out, ALL);

	/**
	 Step 9: Executing the circuit using the ABYParty object evaluate the
	 problem.
	 */
	party->ExecCircuit();

	/**
	 Step 10: Type caste the plaintext output to 16 bit unsigned integer.
	 */
	s_out->get_clear_value_vec(&out_vals, &out_bitlen, &out_nvals);

	std::cout << "A vector: \n";
	for (int i = 0; i < num; i++){
		if (i == 0){
			std::cout << "[";
		}
    	std::cout << xvals[i];
		if (i == num - 1){
			std::cout << "]\n";
		} else {
			std::cout << ",";
		}
	}
		
	std::cout << "B vector: \n";
	for (int i = 0; i < num; i++){
		if (i == 0){
			std::cout << "[";
		}
    	std::cout << yvals[i];
		if (i == num - 1){
			std::cout << "]";
		} else {
			std::cout << ",";
		}
	}

	std::cout << "\nCircuit Result: \n";
	for (int i = 0; i < num; i++){
		if (i == 0){
			std::cout << "[";
		}
    	std::cout << out_vals[i];
		if (i == num - 1){
			std::cout << "]";
		} else {
			std::cout << ",";
		}
	}
	std::cout << '\n';
	delete s_x_vec;
	delete s_y_vec;
	delete party;

	return 0;
}

/*
 Constructs the inner product circuit. num multiplications and num additions.
 */
share* BuildMatrixSubCircuit(share *s_x, share *s_y, uint32_t num, ArithmeticCircuit *ac) {
	uint32_t i;

	// split SIMD gate to separate wires (size many)
	// s_x = ac->PutSplitterGate(s_x);
	// s_y = ac->PutSplitterGate(s_y);

	// // add up the individual multiplication results and store result on wire 0
	// // in arithmetic sharing ADD is for free, and does not add circuit depth, thus simple sequential adding
	// for (i = 0; i < num; i++) {
	// 	s_x->set_wire_id(i, ac->PutSUBGate(s_x->get_wire_id(i), s_y->get_wire_id(i)));
	// }
	
	s_x = ac->PutSUBGate(s_x, s_y);

	return s_x;
}
