#ifndef __graph__
#define __graph__

#include "utils.h"
#include "dmatrix.h"

class Graph {
	
public:
	Graph(const std::string& fname);
	~Graph();

	void print();
	double graph_kernel(Graph* g, ptr2nodekernel fptr, double par, const std::string& name);
	std::string& get_label() { return label; }
	std::string& get_fname() { return graph_fname; }
	
private:
	// number of nodes in this graph
	int n_nodes;
	// number of features at each node
	int n_feats;
	// full path to the original file
	std::string graph_fname;
	// label for this graph
	std::string label;
	// adj matrix
	DMatrix* adj_mat;
	// shortest path adj matrix (will store result of floyd warshall)
	DMatrix* sp_adj_mat;
	// node feature vectors
	DMatrix* feat_vecs;
	
	bool load_graph();
	double spgk(Graph* g, ptr2nodekernel fptr, double par);
	double ngk(Graph* g, ptr2nodekernel fptr, double par);
};

#endif 
