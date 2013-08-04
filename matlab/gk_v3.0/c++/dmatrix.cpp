#include "utils.h"
#include "dmatrix.h"

#include <cmath>

DMatrix::DMatrix(int nrows, int ncols) {
	n_rows = nrows;
	n_cols = ncols;
	create_zero_matrix();
}

DMatrix::~DMatrix() {
	for (int i = 0 ; i < n_rows ; i++) {
		delete data[i];
	}
	delete [] data;
}


void DMatrix::create_zero_matrix() {
	data = new double* [n_rows];
	for (int i = 0 ; i < n_rows ; i ++) {
		data[i] = new double[n_cols];
		for (int j = 0 ; j < n_cols ; j++) {
			data[i][j] = 0;
		}
	}
}

void DMatrix::print(FILE* output) {
	for (int i = 0 ; i < n_rows ; i ++) {
		for (int j = 0 ; j < n_cols ; j ++) {
			fprintf(output, "%g ", data[i][j]);
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
			data[i][j] /= sqrt(data[i][i]*data[j][j]);
			data[j][i] = data[i][j];
		}
		data[i][i] = 1;
	}
}
