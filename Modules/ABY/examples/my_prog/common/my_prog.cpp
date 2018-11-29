/**
 \file 		innerproduct.cpp
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
 \brief		Implementation of the Inner Product using ABY Framework.
 */

#include "my_prog.h"
#include <abycore/sharing/sharing.h>
#include <abycore/circuit/booleancircuits.h>

int32_t test_inner_product_circuit(e_role role, const std::string& address, uint16_t port, seclvl seclvl,
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
			(ArithmeticCircuit*) sharings[S_ARITH]->GetCircuitBuildRoutine();

	BooleanCircuit* circ2 =
			(BooleanCircuit*) sharings[S_BOOL]->GetCircuitBuildRoutine();
	Circuit* yc = (Circuit*) sharings[S_YAO]->GetCircuitBuildRoutine();





	/**
	 Step 4: Creating the share objects - s_x_vec, s_y_vec which
	 are used as inputs to the computation. Also, s_out which stores the output.
	 */

	share *s_x_vec, *s_y_vec, *s_out, *s_out2, *s_out_vec, *s_exit, *s_out_share;

	/**
	 Step 5: Allocate the xvals and yvals that will hold the plaintext values.
	 */
	uint32_t x, y;

	uint32_t *output, *output2, outbitlength, outnvals;

	std::vector<uint16_t> xvals(num);
	std::vector<uint16_t> yvals(num);

	uint16_t i;
	srand(time(NULL));

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

		x = 9;
		y = 5;
		
		
		xvals[i] = x;
		yvals[i] = y;


	
	}

	for (int i=0; i<num; i++){


		if (i==0){
			std::cout << "input a = [" << xvals[i];
		}

		else if (i == num-1){
			std::cout << "," << xvals[i] << "] \n";
		}

		else{
			std::cout << "," << xvals[i];

		}
	
	
	}


	for (int i=0; i<num; i++){

		if (i==0){
			std::cout << "input b = [" << yvals[i];
		}

		else if (i == num-1){
			std::cout << "," << yvals[i] << "] \n";
		}

		else{
			std::cout << "," << yvals[i];

		}
	
	
	}
	
    uint32_t input;
	input = 9;

	s_x_vec = circ2->PutSIMDINGate(num, xvals.data(), 32, SERVER);
	s_y_vec = circ2->PutSIMDINGate(num, yvals.data(), 32, CLIENT);

	/**
	 Step 7: Call the build method for building the circuit for the
	 problem by passing the shared objects and circuit object.
	 Don't forget to type cast the circuit object to type of share
	 */

	//s_out = BuildAddCircuit(s_x_vec, s_y_vec, num,
	//		(ArithmeticCircuit*) circ);

	//s_out = circ2->PutY2BGate(yc->PutA2YGate(s_x_vec));
	
	s_out = circ2->PutFPGate(s_x_vec,s_y_vec,ADD,num,no_status);
	/**
	 Step 8: Output the value of s_out (the computation result) to both parties
	 */
	//s_out2 = BuildSubCircuit(s_out, s_y_vec, num,
	//		(ArithmeticCircuit*) circ);

	s_out = circ2->PutOUTGate(s_out,ALL);
	//s_out2 = circ->PutOUTGate(s_out2, ALL);

	/**
	 Step 9: Executing the circuit using the ABYParty object evaluate the
	 problem.
	 */
	party->ExecCircuit();
	/**
	 Step 10: Type caste the plaintext output to 16 bit unsigned integer.
	 */

	//s_out_share = share* PutSharedINGate(share* s_out)
	s_out->get_clear_value_vec(&output, &outbitlength, &outnvals);
	//s_out2->get_clear_value_vec(&output2, &outbitlength, &outnvals);

	



	for(int i=0; i<num; i++){

		if (i==0){
			std::cout << "sum = [" << output[i];
		}

		else if (i == num-1){
			std::cout << "," << output[i] << "] \n";
		}

		else{
			std::cout << "," << output[i];

		}
	}






// new circuit


	// party ->Reset();


	// s_out_vec = circ->PutSIMDINGate(num, PutSharedINGate(s_out), 16, SERVER);
	// s_x_vec = circ->PutSIMDINGate(num, xvals.data(), 16, CLIENT);

	// // new substraction circuit

	// s_out2 = BuildSubCircuit(s_out_vec, s_y_vec, num,
	// 		(ArithmeticCircuit*) circ);

	// s_out2 = circ->PutOUTGate(s_out2, ALL);

	// party->ExecCircuit();

	// s_out2->get_clear_value_vec(&output2, &outbitlength, &outnvals);

	// //s_out->PutCombinerGate(s_res);
	//std::cout << "\nCircuit Result: " << output2;





	delete s_x_vec;
	delete s_y_vec;
	delete party;

	return 0;
}



/*
 Constructs the inner product circuit. num multiplications and num additions.
 */
share* BuildAddCircuit(share *s_x, share *s_y, uint32_t num, ArithmeticCircuit *ac) {
	uint32_t i;

	// pairwise multiplication of all input values
	s_x = ac->PutADDGate(s_x, s_y);
	// split SIMD gate to separate wires (size many)
	//s_x = ac->PutSplitterGate(s_x);

	// add up the individual multiplication results and store result on wire 0
	// in arithmetic sharing ADD is for free, and does not add circuit depth, thus simple sequential adding
	// for (i = 1; i < num; i++) {
	// 	s_x->set_wire_id(0, ac->PutADDGate(s_x->get_wire_id(0), s_x->get_wire_id(i)));
	// }

	// discard all wires, except the addition result
	//s_x->set_bitlength(1);

	return s_x;
}


share* BuildSubCircuit(share *s_x, share *s_y, uint32_t num, ArithmeticCircuit *ac) {
	uint32_t i;

	s_x = ac->PutSUBGate(s_x, s_y);

	return s_x;
}
