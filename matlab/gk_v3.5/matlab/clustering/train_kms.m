% ------------------------------------------------------------------------------
% ------------------------------------------------------------------------------
% define constants
% ------------------------------------------------------------------------------
if strcmp(computer, 'MACI64')
    % add software to path
    addpath('~/s/libsvm-3.12/matlab');
    % add folders where to look for kernel matrices
    p.km_folders = { ...
        '~/Downloads/clust-covdet/output-24px-500w', ...
        '~/Downloads/clust-covdet/output-32px-500w', ...
    };
end
if strcmp(computer, 'GLNXA64')
    % add software to path
    addpath('~/Software/libsvm-3.12/matlab');
    p.km_folders = { ...
        '~/Desktop/Data/BCCT200_test/Cluster_PHOW/output-24px-750w',
        %'~/Desktop/Data/BCCT200_clust/output-24px-500w',
        %'~/Desktop/Data/BCCT200_clust/output-24px-750w',
        %'~/Desktop/Data/BCCT200_clust/output-24px-150w',
        %'~/Desktop/Data/BCCT200_clust/output-32px-250w',
        %'~/Desktop/Data/BCCT200_clust/output-32px-500w',
        %'~/Desktop/Data/BCCT200_clust/output-32px-750w',
        %'~/Desktop/Data/BCCT200_clust/output-32px-150w',
        
    };
end
% add proper paths
addpath('~/Software/gk-v3.5/matlab/common');

% extension to match kernel matrices
p.extension = 'kernel';
% C values for tuning the SVM
p.c_values = 2.^(-2:1:9);
% plot confusion and roc
p.plot_results = false;

% ------------------------------------------------------------------------------
% ------------------------------------------------------------------------------
% train all kernel matrices
% ------------------------------------------------------------------------------
for f = 1 : numel(p.km_folders)
    folder = p.km_folders{f};
    folds = dir(fullfile(folder,'fold-*'));
    folds = {folds.name};
    % read file names (these kernel matrices must exist on all folds
    fnames = dir(fullfile(folder,folds{1},['*.' p.extension]));
    fnames = {fnames.name};
    n_kms = length(fnames);
    for i = 1 : n_kms
        for c = 1 : numel(p.c_values)
            targets = [];
            outputs = [];
            for k = 1 : numel(folds);
                % read labels and file names
                labels = importdata(fullfile(folder,folds{k},[fnames{i} '.labels']));
                label_set = unique(labels);
                n_labels = length(label_set);
                img_names = importdata(fullfile(folder,folds{k},[fnames{i} '.fnames']));
                % find the indices for this fold
                train_idxs = find(cellfun(@(x) ~isempty(x), strfind(img_names,'train.graph')));
                test_idxs = find(cellfun(@(x) ~isempty(x), strfind(img_names,'test.graph')));
                % get the kernel values
                km = importdata(fullfile(folder,folds{k},fnames{i}));
                tr = [ (1:length(train_idxs))' km(train_idxs,train_idxs) ];
                te = [ (1:length(test_idxs))' km(test_idxs,train_idxs) ];
                % train the model
                model = msvm_train(tr, labels(train_idxs), label_set, n_labels, sprintf('-t 4 -h 0 -c %g', p.c_values(c)));
                [pred, ~] = msvm_test(te, labels(test_idxs), model);
                % save predictions
                targets = [targets ; labels(test_idxs)];
                outputs = [outputs ; pred];
            end
            % generate confusion matrix
            targets_bin = [];
            outputs_bin = [];
            for k = 1 : n_labels
                targets_bin = [targets_bin ; double(strcmp(targets,label_set(k)))'];
                outputs_bin = [outputs_bin ; double(strcmp(outputs,label_set(k)))'];
            end
            % calculate accuracy
            [~, m, ~, ~] = confusion(targets_bin, outputs_bin);
            accuracy = sum(diag(m)) / sum(sum(m));
            % plot results
            [~, m, ~, ~] = confusion(targets_bin, outputs_bin);
            fprintf(1, 'Overall %d-fold CV Accuracy for %s at %s with C (%g):  %g\n', numel(folds), fnames{i}, folder, p.c_values(c), sum(diag(m))/sum(sum(m)));
            if p.plot_results
                disp(m);
                figure('Menubar', 'none'); clf;
                plotconfusion(targets_bin, outputs_bin);
                title(sprintf('%s with C:%g',fnames(i).name,p.c_values(c)), 'Interpreter', 'none');
            end
        end          
    end
end
