/**
 \file 		millionaire_prob.cpp
 \author 	sreeram.sadasivam@cased.de
 \copyright	ABY - A Framework for Efficient Mixed-protocol Secure Two-party Computation
			Copyright (C) 2015 Engineering Cryptographic Protocols Group, TU Darmstadt
			This program is free software: you can redistribute it and/or modify
			it under the terms of the GNU Affero General Public License as published
			by the Free Software Foundation, either version 3 of the License, or
			(at your option) any later version.
			This program is distributed in the hope that it will be useful,
			but WITHOUT ANY WARRANTY; without even the implied warranty of
			MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
			GNU Affero General Public License for more details.
			You should have received a copy of the GNU Affero General Public License
			along with this program. If not, see <http://www.gnu.org/licenses/>.
 \brief		Implementation of the millionaire problem using ABY Framework.
 */

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
	Circuit* circ = sharings[sharing]->GetCircuitBuildRoutine();


	/**
		Step 4: Creating the share objects - s_muA, s_muB, s_AmuA, s_BmuB which
				is used as input to the computation function. Also s_out
				which stores the output.
				We have s_AmuA : A + mu_A
						s_BmuB : b + mu_b
	*/

	share *s_mu_A, *s_mu_B, *s_AmuA, *s_BmuB, *s_out;

	/**
		Step 5: Initialize Alice's and Bob's money with random values.
				Both parties use the same seed, to be able to verify the
				result. In a real example each party would only supply
				one input value.
	*/

	uint32_t mu_A, mu_B, AmuA, BmuB, output;
	// Evaluator inputs
	mu_A = 10;
	mu_B = 20;
	// CSP inputs
	AmuA = 60;
	BmuB = 80;

	//s_alice_money = circ->PutINGate(alice_money, bitlen, CLIENT);
	//s_bob_money = circ->PutINGate(bob_money, bitlen, SERVER);
	if(role == SERVER) {
		s_AmuA = circ->PutINGate(AmuA, bitlen, SERVER);
		s_BmuB = circ->PutINGate(BmuB, bitlen, SERVER);
	} else { //role == Evaluator
		s_mu_A = circ->PutINGate(mu_A, bitlen, CLIENT);
		s_mu_B = circ->PutINGate(mu_B, bitlen, CLIENT);
	}

	/**
		Step 7: Call the build method for building the circuit for the
				problem by passing the shared objects and circuit object.
				Don't forget to type cast the circuit object to type of share
	*/

	s_out = BuildAddCircuit(s_mu_A, s_mu_B, s_AmuA, s_BmuB,
			(BooleanCircuit*) circ);

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

	std::cout << "\nTesting A+muA B+muB substraction " << get_sharing_name(sharing) << " sharing: " << std::endl;
	std::cout << "\nmu_A:\t" << mu_A;
	std::cout << "\nmu_B:\t" << mu_B;
	std::cout << "\nA + mu_A:\t" << AmuA;
	std::cout << "\nB + mu_B:\t" << BmuB;
	std::cout << "\nResult:\t" << output;				

	delete party;
	return 0;
}

share* BuildAddCircuit(share *s_mu_A, share *s_mu_B, share *s_AmuA, share *s_BmuB,
		BooleanCircuit *bc) {

	share *outA, *outB;

	/** Calling the greater than equal function in the Boolean circuit class.*/
	outA = bc->PutSUBGate(s_AmuA, s_mu_A);
	outB = bc->PutSUBGate(s_BmuB, s_mu_B);

	return outA;
}
