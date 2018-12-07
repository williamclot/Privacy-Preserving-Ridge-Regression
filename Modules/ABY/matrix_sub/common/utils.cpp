/*********************************************
Author: William Clot
Email: contact@williamclot.com
Date: 26/11/18
**********************************************/

#include <vector>
#include "utils.h"

using namespace std;

// Simple void function that prints out a vector value to std::cout
void printVector(vector<uint16_t> &vect, int num, string name) {
	cout << name << " vector: \n";
	for (int i = 0; i < num; i++){
		if (i == 0){
			cout << "[";
		}
    	cout << vect[i];
		if (i == num - 1){
			cout << "]\n";
		} else {
			cout << ",";
		}
	}
}