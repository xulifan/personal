#ifndef __dmatrix__
#define __dmatrix__

#include <iostream>

class DMatrix {
public:
	DMatrix(int nrows, int ncols);
	~DMatrix();
	
	int rows() { return n_rows; }
	int cols() { return n_cols; }
	double& at(int r, int c) { return data[r][c]; }
	void set(int r, int c, double val) { data[r][c] = val; }
	double* row(int r) { return data[r]; }

	void symm_set(int r, int c, double val) { data[r][c] = data[c][r] = val; }
	void increment(int r, int c) { data[r][c] ++; }

	void print(FILE* output);
	void normalize();

private:
	int n_cols;
	int n_rows;
	double** data;
	
	void create_zero_matrix();
};

#endif /* defined(__Create_KM__dmatrix__) */
