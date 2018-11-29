#ifndef __MATRIXSUB_H_
#define __MATRIXSUB_H_

#include <abycore/circuit/booleancircuits.h>
#include <abycore/circuit/arithmeticcircuits.h>
#include <abycore/circuit/circuit.h>
#include <abycore/aby/abyparty.h>
#include <math.h>
#include <cassert>


/**
 \param		role 		role played by the program which can be server or client part.
 \param 	address 	IP Address
 \param 	seclvl 		Security level
 \param 	nvals		Number of values
 \param 	bitlen		Bit length of the inputs
 \param 	nthreads	Number of threads
 \param		mt_alg		The algorithm for generation of multiplication triples
 \param 	sharing		Sharing type object
 \param 	num			the number of elements in the inner product
 \brief		This function is used for running a testing environment for solving the
 Inner Product.
 */
int32_t test_matrix_sub_circuit(e_role role, const std::string& address, uint16_t port, seclvl seclvl,
		uint32_t nvals, uint32_t bitlen, uint32_t nthreads, e_mt_gen_alg mt_alg,
		e_sharing sharing, uint32_t num);

/**
 \param		s_x			share of X values
 \param		s_y 		share of Y values
 \param 	num			the number of elements in the inner product
 \param		ac	 		Arithmetic Circuit object.
 \brief		This function is used to build and solve the Inner Product modulo 2^16. It computes the inner product by
 	 	 	multiplying each value in x and y, and adding those multiplied results to evaluate the inner
 	 	 	product. The addition is performed in a tree, thus with logarithmic depth.
 */
share* BuildMatrixSubCircuit(share *s_x, share *s_y, uint32_t num, ArithmeticCircuit *ac);

#endif
