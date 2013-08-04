#include "utils.h"
#include "graph.h"

#include <vector>
#include <sstream>
#include <stdlib.h>
#include <dirent.h>
#include <pthread.h>

struct ThreadInfo {
	int my_id;
	int n_threads;
	int n_graphs;
	double node_kern_param;
	DMatrix* km;
	std::string* gk_type;
	std::vector<Graph*>* graphs;
	std::vector<std::string>* labels;
	std::vector<std::string>* fnames;
	ptr2nodekernel node_kern;
};

void* threaded_gk(void* args) {
	ThreadInfo* d = (ThreadInfo*) args;
	// lets see some action
	for (int i = 0, k = 0 ; i < d->n_graphs ; i++) {
		if (d->my_id == 0) {
			d->labels->at(i) = d->graphs->at(i)->get_label();
			d->fnames->at(i) = d->graphs->at(i)->get_fname();
		}
		for (int j = i ; j < d->n_graphs ; j++, k++) {
			if ((k % d->n_threads) == d->my_id) {
				d->km->symm_set(i, j, d->graphs->at(i)->graph_kernel(d->graphs->at(j),d->node_kern,d->node_kern_param,*d->gk_type));
			}
		}
	}
	// end of the job
	pthread_exit(NULL);
}

int main(int argc, const char * argv[])
{
	//---------------------------------------------------------------------------
	// build the map that holds all the user params
	std::map<std::string, std::string> params;
	parse_params(params, argc, argv);
	
	// remove trailing '/' from folder names
	r_trim(params["input_folder"], "/");
		
	//---------------------------------------------------------------------------
	// iterate files in input folder and load the graphs
	std::cout << "Log: Loading the graphs ..." << std::endl;
	std::vector<Graph*> graphs;
	struct dirent *dp;
	DIR *dirp = opendir(params["input_folder"].c_str());
	while ((dp = readdir(dirp)) != NULL) {
		std::string fname(dp->d_name);
		if (fname.length() > 6 && ! fname.compare(fname.length()-6,6,".graph")) {
			std::ostringstream fullname(std::ostringstream::out);
			fullname << params["input_folder"] << "/" << fname;
			graphs.push_back(new Graph(fullname.str()));
		}
	}
	closedir(dirp);

	//---------------------------------------------------------------------------
	// create a common name for saving the kernel matrix 
	std::ostringstream common_fname(std::ostringstream::out);
	common_fname << params["input_folder"] << '/' << params["vtx_kern"] << "-" << params["vtx_kern_param"] << "-" << params["graph_kern"];
	
	//---------------------------------------------------------------------------
	// calculate the kernel matrix for the graphs
	int n_graphs = graphs.size();
	int n_threads = atoi(params["n_threads"].c_str());
	std::vector<std::string> labels(n_graphs);
	std::vector<std::string> fnames(n_graphs);
	std::cout << "Log: Creating KM using " << n_threads << " threads ..." << std::endl;
	DMatrix graph_km(n_graphs, n_graphs);
	// create all the threads
	pthread_t threads[n_threads];
	ThreadInfo thread_args[n_threads];
	for (int i = 0 ; i < n_threads ; ++i) {
		thread_args[i].my_id = i;
		thread_args[i].n_threads = n_threads;
		thread_args[i].n_graphs = n_graphs;
		thread_args[i].km = &graph_km;
		thread_args[i].graphs = &graphs;
		thread_args[i].labels = &labels;
		thread_args[i].fnames = &fnames;
		thread_args[i].gk_type = &params["graph_kern"];
		thread_args[i].node_kern = choose_node_kernel(params["vtx_kern"]);
		thread_args[i].node_kern_param = atof(params["vtx_kern_param"].c_str());
		pthread_create(&threads[i], NULL, threaded_gk, (void*) &thread_args[i]);
	}
	// wait until the threads finish the job
	for (int i = 0 ; i < n_threads ; ++i) {
		pthread_join(threads[i], NULL);
	}
	std::cout << "Log: KM created" << std::endl;
	// normalize the kernel matrix
	//graph_km.print(stdout);
	graph_km.normalize();
	// save the normalized kernel matrix
	std::string km_fname = common_fname.str() + ".kernel";
	FILE *km_fid = fopen(km_fname.c_str(), "wt");
	graph_km.print(km_fid);
	fclose(km_fid);
	// save the labels and fnames
	std::string fnames_fname = km_fname + ".fnames";
	std::string labels_fname = km_fname + ".labels";
	FILE *labels_fid = fopen(labels_fname.c_str(), "wt");
	FILE *fnames_fid = fopen(fnames_fname.c_str(), "wt");
	for (int i = 0 ; i < n_graphs ; i ++) {
		fprintf(labels_fid, "%s\n", labels[i].c_str());
		fprintf(fnames_fid, "%s\n", fnames[i].c_str());
	}
	fclose(labels_fid);
	fclose(fnames_fid);

	//---------------------------------------------------------------------------
	// free memory
	for (int i = 0 ; i < n_graphs ; i ++) {
		delete graphs[i];
	}

	//---------------------------------------------------------------------------
	// succesfully ends the program
	return EXIT_SUCCESS;
}

