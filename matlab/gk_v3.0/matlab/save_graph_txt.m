function save_graph_txt(fname, g, p)
    % get linear indexing of interesting nodes
    idxs = find(g.interesting);
    n_nodes = numel(idxs);
    n_feats = size(g.histograms{1,1},2);
    if n_nodes == 0
        return;
    end
    % create file
    fid = fopen(fname, 'wt');
    % print number of nodes and lenght of feature vectors
    fprintf(fid, '%d %d\n', n_nodes, n_feats);
    % print all histograms
    for i = 1 : n_nodes
        h = g.histograms{idxs(i)};
        for j = 1 : n_feats
            fprintf(fid, '%g ', h(j));
        end
        fprintf(fid, '\n');
    end
    % print the adjacency matrix
    adj_mat = [];
    labels = {};
    for i = 1 : n_nodes
        node_map = zeros(size(g.interesting));
        node_map(idxs(i)) = 1;
        [rr, cc] = ind2sub(size(g.interesting), idxs(i));
        labels{i} = sprintf('%d,%d', rr, cc);
        if p.n_neighbors == 8
            neighbors = find(bwdist(node_map,'chessboard') == 1);
        elseif p.n_neighbors == 4
            neighbors = find(bwdist(node_map,'cityblock') == 1);
        end
        adj_row = zeros(1, n_nodes);
        adj_row(arrayfun(@(x) find(idxs==x), intersect(neighbors,idxs))) = 1;
        for j = 1 : n_nodes
            fprintf(fid, '%g ', adj_row(j));
        end
        fprintf(fid, '\n');
        adj_mat = [adj_mat ; adj_row];
    end
    fclose(fid);
    % draw connections
    if p.plot_wanted
        bg = biograph(tril(adj_mat), labels, 'ShowArrow', 'off');
        dolayout(bg);
        for i = 1 : n_nodes
            [rr, cc] = ind2sub(size(g.interesting), idxs(i));
            bg.nodes(i).Position = [30*cc 30*(g.n_row_tiles-rr+1)];
        end
        dolayout(bg, 'Pathsonly', true);
        view(bg);
        disp('Press any key to continue ...');
        pause; close all;
        child_handles = allchild(0);
        names = get(child_handles, 'Name');
        k = find(strncmp('Biograph Viewer', names, 15));
        close(child_handles(k));
    end