#include "add.h"
#include <abycore/circuit/booleancircuits.h>
#include <abycore/sharing/sharing.h>

int32_t test_add_circuit(e_role role, const std::string& address, uint16_t port, seclvl seclvl,
		uint32_t nvals, uint32_t bitlen, uint32_t nthreads, e_mt_gen_alg mt_alg,
		e_sharing sharing) {

	/**
		Step 1: Create the ABYParty object which defines the basis of all the
		 	 	operations which are happening.	Operations performed are on the
		 	 	basis of the role played by this object.
	*/
	ABYParty* party = new ABYParty(role, address, port, seclvl, bitlen, nthreads, mt_alg);

	/**
		Step 2: Get to know all the sharing types available in the program.
	*/

	std::vector<Sharing*>& sharings = party->GetSharings();

	/**
		Step 3: Create the circuit object on the basis of the sharing type
				being inputed.
	*/
	Circuit* circ = sharings[sharing]->GetCircuitBuildRoutine();


	/**
		Step 4: Creating the share objects - s_A and s_B which
				is used as input to the computation function. Also s_out
				which stores the output.
	*/

	share *s_A, *s_B, *s_out;

	/**
		Step 5: Initialize Alice's and Bob's money with random values.
				Both parties use the same seed, to be able to verify the
				result. In a real example each party would only supply
				one input value.
	*/

	uint32_t A, B, output;
	// Evaluator inputs
	A = 10;
	B = 10;

	if(role == SERVER) {
		s_A = circ->PutINGate(A, bitlen, SERVER);
		s_B = circ->PutDummyINGate(bitlen);
	} else { //role == Evaluator
		s_A = circ->PutDummyINGate(bitlen);
		s_B = circ->PutINGate(B, bitlen, CLIENT);
	}

	/**
		Step 7: Call the build method for building the circuit for the
				problem by passing the shared objects and circuit object.
				Don't forget to type cast the circuit object to type of share
	*/

	s_out = BuildAddCircuit(s_A, s_B, (BooleanCircuit*) circ);

	/**
		Step 8: Modify the output receiver based on the role played by
				the server and the client. This step writes the output to the
				shared output object based on the role.
	*/
	s_out = circ->PutOUTGate(s_out, ALL);

	/**
		Step 9: Executing the circuit using the ABYParty object evaluate the
				problem.
	*/
	party->ExecCircuit();

	/**
		Step 10:Type casting the value to 32 bit unsigned integer for output.
	*/
	output = s_out->get_clear_value<uint32_t>();

	std::cout << "\nTesting A+B addition " << get_sharing_name(sharing) << " sharing: " << std::endl;
	std::cout << "\nA:\t" << A;
	std::cout << "\nB:\t" << B;
	std::cout << "\nA + B:\t" << output << std::endl;

	delete party;
	return 0;
}

share* BuildAddCircuit(share *s_A, share *s_B, BooleanCircuit *bc) {

	share *out;

	/** Calling the greater than equal function in the Boolean circuit class.*/
	out = bc->PutADDGate(s_A, s_B);

	return out;
}
