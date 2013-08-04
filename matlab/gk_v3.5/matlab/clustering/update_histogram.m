function histograms = update_histogram(g, n_clusters, tree, vocab)
    histograms = cell(size(g.histograms));
    for i = 1 : g.n_row_tiles
        for j = 1 : g.n_col_tiles
            % compute histogram for tile
            clusters = vl_kdtreequery(tree, vocab, single(g.descriptors{i,j})');
            histograms{i,j} = histc(clusters, 1:n_clusters);
            histograms{i,j} = histograms{i,j} / sum(histograms{i,j});
        end
    end
    