% ------------------------------------------------------------------------------
% ------------------------------------------------------------------------------
% define constants
% ------------------------------------------------------------------------------
if strcmp(computer, 'MACI64')
    % add software to path
    addpath('~/s/libsvm-3.12/matlab');
    % add folders where to look for kernel matrices
    p.km_folders = { ...
        '~/Downloads/gk3-covdet/output-24px', ...
        '~/Downloads/gk3-sift/output-24px', ...
    };
end
if strcmp(computer, 'GLNXA64')
    % add software to path
    addpath('~/Software/libsvm-3.12/matlab');
    p.km_folders = { ...
        %'/home/lifan/Desktop/Data/Malware/set3/',...
        %'~/Desktop/Data/1518b_2658g_100f_normalized/',...
        '~/Desktop/svm_results/sudhee_results/test/',...
        
        %'~/Desktop/svm_results/sudhee_results/updated',...
        %'~/Desktop/Data/scene-15-test/COVDET/4_neighbors/output-40px/',
    };
end
% extension to match kernel matrices
p.extension = 'kernel';
% number of folds for cross validation
p.n_folds = 10;
% number of times CV should be repeated
p.n_repeats = 1;
% C values for tuning the SVM
%p.c_values = 2.^(-2:1:9);
p.c_values = 2.^9;
% plot confusion and roc
%p.plot_results = false;
p.plot_results = true;

% ------------------------------------------------------------------------------
% ------------------------------------------------------------------------------
% train all kernel matrices
% ------------------------------------------------------------------------------
rng('shuffle');
for f = 1 : numel(p.km_folders)
    folder = p.km_folders{f};
    folder
    % read file names
    fnames = dir(fullfile(folder,['*.' p.extension]));
    n_kms = length(fnames);
    for i = 1 : n_kms
        % load labels
        labels = importdata(fullfile(folder,[fnames(i).name '.labels']));
        num_files=size(labels,1);
        %num_files
        files = importdata(fullfile(folder,[fnames(i).name '.fnames']));
        label_set = unique(labels);
        n_labels = length(label_set);
        % load kernel matrix
        km_fname = fullfile(folder, fnames(i).name);
        km = importdata(km_fname);
        % do reapeated cross validation
        accuracies = zeros(p.n_repeats, numel(p.c_values));
        %fprintf('Repeats => ');
        for n = 1 : p.n_repeats
            % create indices for CV
            scv = cvpartition(labels, 'kfold', p.n_folds);
            % try different C values for SVM
            for c = 1 : numel(p.c_values)
                targets = [];
                outputs = [];
                for k = 1 : scv.NumTestSets
                    % find the indices for this fold
                    test_idxs = find(scv.test(k));
                    train_idxs = find(scv.training(k));
                    % get the kernel values
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
                for k = 1: num_files
                    if targets_bin(1,k) ~= outputs_bin(1,k)
                        %fprintf('%s\n',files{k})
                    end
                end
                % calculate accuracy
                [~, m, ~, ~] = confusion(targets_bin, outputs_bin);
                accuracies(n,c) = sum(diag(m))/sum(sum(m));
                % plot results
                if p.plot_results
                    disp(m);
                    %m(1,2)
                    %m(2,1)
                    %figure('Menubar', 'none'); clf;
                    %plotconfusion(targets_bin, outputs_bin);
                    %title(fnames(i).name, 'Interpreter', 'none');
                    fprintf(1,'FN rate is %g\n',m(1,2)/(m(1,2)+m(1,1)));
                    fprintf(1,'FP rate is %g\n',m(2,1)/(m(2,1)+m(2,2)));
                end
            end
            %fprintf('%d ', n);
        end
        %fprintf('\n', n);
        for c = 1 : numel(p.c_values)
            fprintf(1, 'Overall %dx%d-fold CV Acc for %s on %s with C (%g):  %g\n', p.n_repeats, p.n_folds, fnames(i).name, folder, p.c_values(c), sum(accuracies(:,c))/p.n_repeats);
        end
    end
end