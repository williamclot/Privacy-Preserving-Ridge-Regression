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

void test_circuit(e_role role, const std::string& address, uint16_t port, seclvl seclvl, uint32_t nvals, uint32_t nthreads,
	e_mt_gen_alg mt_alg, e_sharing sharing, std::vector<double> data);

share* MatrixSubstraction(share *s_A, share *s_B, BooleanCircuit *bc, uint32_t nvals);

share* Cholesky(share *A, share *L, share *zero_share, share *half, uint32_t bitlen, uint32_t nvals, ArithmeticCircuit *ac, BooleanCircuit *bc, Circuit *yc);

share* SqurtApprox(share *s_x, share *half, uint32_t step, ArithmeticCircuit *ac, BooleanCircuit *bc, Circuit *yc); 

share* ExtractIndex(share *s_x , uint32_t i, uint32_t bitlen, ArithmeticCircuit *ac, BooleanCircuit *bc, Circuit *yc);
