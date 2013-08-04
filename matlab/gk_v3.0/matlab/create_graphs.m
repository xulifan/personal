%%
% ------------------------------------------------------------------------------
% ------------------------------------------------------------------------------
% define constants
% ------------------------------------------------------------------------------
if strcmp(computer, 'MACI64')
    % add software to path
    run('~/s/vlfeat-0.9.16/toolbox/vl_setup');
    % path to the input data folder
    p.data_folder = '~/d/HLD_Navy/BCCT200';
    % path to the output data folder
    p.output_root = '~/Downloads/gk3-covdet';
end
if strcmp(computer, 'GLNXA64')
    % add software to path
    run('~/Software/vlfeat-0.9.16/toolbox/vl_setup');
    % path to the input data folder
    %p.data_folder = '~/Desktop/Data/BCCT200';
    p.data_folder = '~/Desktop/Data/scene-15-renamed';
    % path to the output data folder
    p.output_root = '~/Desktop/Data/scene-15-test/LBP/8_neighbors';
end
% number of pixels for each tile
%p.n_px = [16 24 32 40];
p.n_px = [24 32 40];
% maximum number of columns or rows in an image
p.max_img_len = 300;
% number of neighbors to consider when building the graph
% can be either 4 or 8
p.n_neighbors = 8;
% feature type
% can be either LBP or SIFT or PHOW or COVDET
p.feat_type = 'LBP';
% enable plots?
p.plot_wanted = false;

%%
% ------------------------------------------------------------------------------
% ------------------------------------------------------------------------------
% iterate over all files creating the graphs
% ------------------------------------------------------------------------------
class_names = dir(p.data_folder);
class_names = class_names([class_names.isdir]);
class_names = {class_names(3:end).name};

for npx = p.n_px
    output_folder = fullfile(p.output_root, sprintf('output-%dpx', npx));
    % make sure output folder exists
    if exist(output_folder, 'file')
        rmdir(output_folder, 's');
    end
    mkdir(output_folder);
    % process files
    for i = 1 : length(class_names)
        fnames = dir(fullfile(p.data_folder, class_names{i}, '*g'));
        n_graphs = length(fnames);
        for j = 1 : n_graphs
            % create a graph from file
            graph = build_graph(fullfile(p.data_folder,class_names{i},fnames(j).name), npx, p);
            % remove uninformative nodes
            graph.interesting = remove_nodes(graph, p.plot_wanted);
            % save graph
            save_graph_txt(fullfile(output_folder, [fnames(j).name, '.graph']), graph, p);
        end
    end
end
