#ifndef __utils__
#define __utils__

#include <map>
#include <fstream>

#include "dmatrix.h"

class MyTimer {
	private:
		double start;
		double get_current_time();
	public:
		MyTimer();
		double elapsed();
		void restart();
};

typedef double(*ptr2nodekernel)(const double* r, const double* s, int n, double p);

void r_trim(std::string& s, const std::string& del);
void l_trim(std::string& s, const std::string& del);
void trim(std::string& s, const std::string& del);

void parse_params(std::map<std::string,std::string>& params, int argc, const char* argv[]);
void read_trimmed_line(std::ifstream& file, std::string& s);

ptr2nodekernel choose_node_kernel(const std::string& name);
double intersection_kernel(const double* r, const double* s, int n, double p);
double gaussian_kernel(const double* r, const double* s, int n, double p);

#endif
