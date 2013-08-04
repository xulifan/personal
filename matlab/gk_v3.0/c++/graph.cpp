#include "graph.h"
#include "utils.h"

#include <cmath>
#include <limits>
#include <sstream>

//----------------------------------------------------------------------
//----------------------------------------------------------------------
Graph::Graph(const std::string& fname) {
	// init members
	graph_fname = fname;
	// load graph as is
	load_graph();
	// update label
	label = fname.substr(fname.find_last_of("/") + 1);
	label = label.substr(0, label.find_first_of("_"));
}

//----------------------------------------------------------------------
//----------------------------------------------------------------------
Graph::~Graph() {
	delete adj_mat;
	delete sp_adj_mat;
	delete feat_vecs;
}

//----------------------------------------------------------------------
//----------------------------------------------------------------------
bool Graph::load_graph() {
	std::string line, token;
	// open file
	std::ifstream graph_file(graph_fname.c_str(), std::ifstream::in);
	if (graph_file.good()) {
		// read first line (nodes and feats)
		read_trimmed_line(graph_file, line);
		std::istringstream iss(line, std::istringstream::in);
		iss >> n_nodes >> n_feats;
		// create space for all feature vectors
		feat_vecs = new DMatrix(n_nodes, n_feats);
		// read all feature vectors
		for (int i = 0 ; i < n_nodes ; i ++) {
			read_trimmed_line(graph_file, line);
			std::istringstream feats(line, std::istringstream::in);
			for (int j = 0 ; j < n_feats ; j ++) {
				feats >> feat_vecs->at(i,j);
			}
		}
		// create space for adjacency matrix
		adj_mat = new DMatrix(n_nodes, n_nodes);
		// read adjacency matrix
		for (int i = 0 ; i < n_nodes ; i ++) {
			read_trimmed_line(graph_file, line);
			std::istringstream weights(line, std::istringstream::in);
			for (int j = 0 ; j < n_nodes ; j ++) {
				weights >> adj_mat->at(i,j);
			}
		}
		// create space for shortest path adjacency matrix
		sp_adj_mat = new DMatrix(n_nodes, n_nodes);
		// transform sp adjacency matrix before applying flod warshall
		for (int i = 0 ; i < n_nodes ; i ++) {
			for (int j = 0 ; j < n_nodes ; j ++) {
				if (i != j) {
					if (adj_mat->at(i,j) == 0) {
						sp_adj_mat->set(i, j, std::numeric_limits<double>::infinity());
					} else {
						sp_adj_mat->set(i, j, adj_mat->at(i, j));
					}
				}
				// else ignore self-loops (already 0)
			}
		}
		// apply floyd warshal to the adj matrix
		for (int k = 0 ; k < n_nodes ; k ++) {
			for (int i =  0 ; i < n_nodes ; i ++) {
				for (int j = 0 ; j < n_nodes ; j ++) {
					sp_adj_mat->set(i, j, std::min(sp_adj_mat->at(i,j), sp_adj_mat->at(i,k)+sp_adj_mat->at(k,j)));
				}
			}
		}
		// close file
		graph_file.close();
		std::cout << "Log: " << n_nodes << " nodes read from " << graph_fname << std::endl;
		return true;
	}
	return false;
}

//----------------------------------------------------------------------
//----------------------------------------------------------------------
double Graph::ngk(Graph* g, ptr2nodekernel fptr, double par) {
	// calculate the vertex kernel for all nodes
	double vk[n_nodes][g->n_nodes];
	for (int i = 0 ; i < n_nodes ; ++ i) {
		for (int j = 0 ; j < g->n_nodes ; ++ j) {
			vk[i][j] = (*fptr)(feat_vecs->row(i), g->feat_vecs->row(j), feat_vecs->cols(), par);
		}
	}
	// calculate the final neighbor kernel
	double gk = 0;
	double neighbors;
	for (int i = 0 ; i < n_nodes ; i ++) {
		for (int j = 0 ; j < g->n_nodes ; j ++) {
			// calculate neighbors kernel
			neighbors = 0;
			for (int m = 0 ; m < n_nodes ; m ++) {
				if (adj_mat->at(i,m) != 0) {
					for (int n = 0 ; n < g->n_nodes ; n ++) {
						if (g->adj_mat->at(j,n) != 0) {
							neighbors += vk[m][n];
						}
					}
				}
			} 
			gk += (vk[i][j] * (1 + neighbors));
		}
	}
	return gk;
}

//----------------------------------------------------------------------
//----------------------------------------------------------------------
double Graph::spgk(Graph* g, ptr2nodekernel fptr, double par) {
	// calculate the vertex kernel for all nodes
	double vk[n_nodes][g->n_nodes];
	for (int i = 0 ; i < n_nodes ; ++ i) {
		for (int j = 0 ; j < g->n_nodes ; ++ j) {
			vk[i][j] = (*fptr)(feat_vecs->row(i), g->feat_vecs->row(j), feat_vecs->cols(), par);
		}
	}
	// calculate final sp graph kernel
	double spgk = 0;
	for (int i = 0 ; i < n_nodes ; ++ i) {
		for (int j = 0 ; j < n_nodes ; ++ j) {
			if (sp_adj_mat->at(i,j) != std::numeric_limits<double>::infinity() && sp_adj_mat->at(i,j) != 0) {
				for (int m = 0 ; m < g->n_nodes ; m ++) {
					for (int n = 0 ; n < g->n_nodes ; n ++) {
						if (g->sp_adj_mat->at(m,n) != std::numeric_limits<double>::infinity() && g->sp_adj_mat->at(m,n) != 0) {
							double wk = std::max(0.0, 3 - fabs(sp_adj_mat->at(i,j)-g->sp_adj_mat->at(m,n)));
							if (wk > 0) {
								spgk += (wk * vk[i][m] * vk[j][n]);
							}
						}
					}
				}
			}
		}
	}
	return spgk;
}

//----------------------------------------------------------------------
//----------------------------------------------------------------------
double Graph::graph_kernel(Graph* g, ptr2nodekernel fptr, double par, const std::string& name) {
	if (!name.compare("SP")) {
		return spgk(g, fptr, par);
	} else if (!name.compare("UNORD")) {
		return ngk(g, fptr, par);
	}
	return -1;
}

//----------------------------------------------------------------------
//----------------------------------------------------------------------
void Graph::print() {
	std::cout << graph_fname << std::endl;
	std::cout << "feature vectors:" << std::endl;
	feat_vecs->print(stdout);
	std::cout << "adjacency matrix:" << std::endl;
	adj_mat->print(stdout);
	std::cout << "shortest path adjacency matrix:" << std::endl;
	sp_adj_mat->print(stdout);
	std::cout << std::endl;
}
