%%
% ------------------------------------------------------------------------------
% ------------------------------------------------------------------------------
% define constants
% ------------------------------------------------------------------------------
% add software to path
if strcmp(computer, 'MACI64')
    % add software to path
    run('~/s/vlfeat-0.9.16/toolbox/vl_setup');
    % path to the input data folder
    p.data_folder = '~/d/HLD_Navy/BCCT200';
    % path to the output data folder
    p.output_root = '~/Downloads/lifanclust-covdet';
end
if strcmp(computer, 'GLNXA64')
    % add software to path
    run('~/Software/vlfeat-0.9.16/toolbox/vl_setup');
    % path to the input data folder
    p.data_folder = '~/Desktop/Data/101_all';
    % path to the output data folder
    p.output_root = '~/Desktop/Data/101_all_test/Cluster_COVDET';
end
% add proper paths
addpath('~/Software/gk-v3.5/matlab/common');
% number of pixels for each tile
p.n_px = [32];
% maximum number of columns or rows in an image
p.max_img_len = 300;
% number of neighbors to consider when building the graph
% can be either 4 or 8
p.n_neighbors = 4;
% feature type
% can be either SIFT or COVDET or PHOW
p.feat_type = 'COVDET';
% this option is only for making the descriptors add up to 1
p.normalize_descriptor = false;
% enable plots?
p.plot_wanted = false;
% number of words used for clustering, i.e. number of clusters
p.n_words = [1500];
% number of folds used for cross validation
p.n_folds = 10;
% maximum number of samples considered for clustering
%p.max_n_samples = 20000;
p.max_n_samples = 100000;

%%
% ------------------------------------------------------------------------------
% ------------------------------------------------------------------------------
% cluster all descriptors
% ------------------------------------------------------------------------------
% get class names
class_names = find_class_names(p.data_folder);
% read all file names
fnames = {};
labels = {};
for i = 1 : length(class_names)
    files = dir(fullfile(p.data_folder, class_names{i}, '*g'))';
    files = cellfun(@(x) fullfile(class_names{i},x), {files.name}, 'UniformOutput', false);
    fnames = [fnames files];    
    labels = [labels repmat(class_names(i),1,numel(files))];
end
% read all images
fprintf(1, 'Reading all images ...\n');
all_imgs = cell(1, numel(fnames));
for i = 1 : numel(fnames)
    all_imgs{i} = read_standardized_img(fullfile(p.data_folder,fnames{i}), p.max_img_len);
end
% create indices for CV
rng('shuffle');
scv = cvpartition(labels, 'kfold', p.n_folds);
% iterate over all folds clustering the descriptors for training samples
vocabs = cell(numel(p.n_words), p.n_folds);
kd_trees = cell(numel(p.n_words), p.n_folds);
for k = 1 : scv.NumTestSets
    % find train indices
    train_idxs = find(scv.training(k));
    % read all descriptors
    fprintf(1, 'Gettting all descriptors for images in fold %d ...\n', k);
    descriptors = {};
    for i = 1 : length(train_idxs)        
        [~, descriptors{i}] = get_img_sift_descriptors(all_imgs{train_idxs(i)}, p);
    end
    % sample if needed
    descriptors = single(cat(2,descriptors{:}));
    if size(descriptors,2) > p.max_n_samples
        descriptors = vl_colsubset(descriptors, p.max_n_samples);        
    end
    fprintf(1, 'Clustering %d descriptors in fold %d ...\n', size(descriptors, 2), k);
    % cluster and build all kdtrees (centroid indexing) for this fold
    for i = 1 : numel(p.n_words)
        vocabs{i,k} = vl_kmeans(descriptors, p.n_words(i), 'verbose', 'algorithm', 'elkan', 'initialization', 'plusplus', 'NumRepetitions', 3);
        kd_trees{i,k} = vl_kdtreebuild(vocabs{i,k});
    end    
end

%%
% ------------------------------------------------------------------------------
% ------------------------------------------------------------------------------
% iterate over all files saving the graphs
% ------------------------------------------------------------------------------
for k = 1 : numel(p.n_words)
    for npx = p.n_px
        % create an empty folder for this pair of #words and #px
        out_folder = fullfile(p.output_root, sprintf('output-%dpx-%dw',npx,p.n_words(k)));
        if exist(out_folder, 'file')
            rmdir(out_folder, 's');    
        end
        mkdir(out_folder);
        % iterate over all folds saving the respective training and test graphs
        for i = 1 : scv.NumTestSets
            % create folder for this fold
            fold_folder = fullfile(out_folder,sprintf('fold-%d',i));
            mkdir(fold_folder);
            % mark training and test images
            img_type = repmat({'train'}, 1, numel(all_imgs));
            [img_type{scv.test(i)}] = deal('test');
            % process all images
            for ii = 1 : numel(all_imgs)
                fprintf(1, 'Creating/Saving graph %s in fold %d ...\n', fnames{ii}, i);
                % create the graph
                graph = build_graph(fullfile(p.data_folder,fnames{ii}), npx, p);
                % update the histogram
                graph.histograms = update_histogram(graph, p.n_words(k), kd_trees{k,i}, vocabs{k,i});
                % remove uninformative nodes based on mean intensity and
                % histogram (all zeros and all nan discarded)
                graph.interesting = remove_nodes(graph, p);
                [~, img_name, ~] = fileparts(fnames{ii});
                % save the graph as a txt file
                save_graph_txt(fullfile(fold_folder, [img_name,'-',img_type{ii},'.graph']), graph, p);
            end
        end
    end
end
