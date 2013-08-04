#include "utils.h"

#include <cmath>
#include <stdlib.h>
#include <sys/time.h>

MyTimer::MyTimer() {
	restart();
}

void MyTimer::restart() {
	start = get_current_time();
}

double MyTimer::get_current_time() {
	struct timeval tp;
	gettimeofday(&tp, NULL);
	return static_cast<double>(tp.tv_sec) + (static_cast<double>(tp.tv_usec)/1E6);
}

double MyTimer::elapsed() {
	// elapsed time in seconds
	return get_current_time() - start;
}

void r_trim(std::string& s, const std::string& del = " \f\n\r\t\v") {
	s.erase(s.find_last_not_of(del) + 1);
}

void l_trim(std::string& s, const std::string& del = " \f\n\r\t\v") {
	s.erase(0, s.find_first_not_of(del));
}

void trim(std::string& s, const std::string& del = " \f\n\r\t\v") {
	r_trim(s, del);
	l_trim(s, del);
}

void parse_params(std::map<std::string,std::string>& params, int argc, const char* argv[]) {
	// check the number of parameters
	// hist_type can be SG or CG (simple or cumulative n-grams)
	if (argc != 6) {
		std::cout << "Usage: create-km <input_folder> <vtx_kern> <vtx_kern_param> <graph_kern> <n_threads>" << std::endl;
		std::cout << "\tpossible values for 'vtx_kern' (type of vertex kernel) are: INTERSECT and GAUSS" << std::endl;
		std::cout << "\tpossible values for 'graph_kern' (kernel for graphs) are: SP, UNORD" << std::endl;
		exit(EXIT_SUCCESS);
	}
	// load parameters into the map
	params["input_folder"] = argv[1];
	params["vtx_kern"] = argv[2];
	params["vtx_kern_param"] = argv[3];
	params["graph_kern"] = argv[4];
	params["n_threads"] = argv[5];
}

void read_trimmed_line(std::ifstream& file, std::string& s) {
	// read line from file
	getline(file, s);
	// trim
	trim(s);
}

ptr2nodekernel choose_node_kernel(const std::string& name) {
	if (!name.compare("GAUSS")) {
		return &gaussian_kernel;
	} else if (!name.compare("INTERSECT")) {
		return &intersection_kernel;
	}
	return NULL;
}

// unused param
double intersection_kernel(const double* r, const double* s, int n, double p) {
	double ik = 0;
	
	for (int k = 0 ; k < n ; k ++) {
		ik += std::min(r[k], s[k]);
	}
	
	return ik;
}

// param p is DD2 (2 * delta^2)
double gaussian_kernel(const double* r, const double* s, int n, double p) {
	double sum_diff = 0;
	
	for (int k = 0 ; k < n ; k++) {
		sum_diff += ((r[k]-s[k]) * (r[k]-s[k]));
	}
	
	return exp(-sum_diff / p);
}
