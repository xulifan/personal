#include "utils.h"
#include "dmatrix.h"

#include <cmath>

DMatrix::DMatrix(int nrows, int ncols) {
	n_rows = nrows;
	n_cols = ncols;
	create_zero_matrix();
}

DMatrix::~DMatrix() {
	delete [] data;
}


void DMatrix::create_zero_matrix() {
	int n = n_rows * n_cols;
	data = new double[n];
	for (int i = 0 ; i < n ; i ++) {
		data[i] = 0;
	}
}

void DMatrix::print(FILE* output) {
	for (int i = 0, k = 0 ; i < n_rows ; i ++) {
		for (int j = 0 ; j < n_cols ; j ++) {
			fprintf(output, "%g ", data[k++]);
		}
		fprintf(output, "\n");
	}
}

void DMatrix::normalize() {
	if (n_rows != n_cols) {
		std::cerr << "Error: " << " Cannot normalize a non-square matrix." << std::endl;
		return;
	}
	// normalize the kernel matrix
	for (int i = 0 ; i < n_rows ; ++ i) {
		for (int j = i+1 ; j < n_rows ; ++ j) {
			data[n_cols*i+j] /= sqrt(data[n_cols*i+i]*data[n_cols*j+j]);
			data[n_cols*j+i] = data[n_cols*i+j];
		}
		data[n_cols*i+i] = 1;
	}
}
