function histograms = find_lbp_features(g)
    % prepare for applying LBP
    mapping = getmaplbphf(8);
    histograms = cell(g.n_row_tiles, g.n_col_tiles);
    % traverse all nodes (tiles)
    for i = 1 : g.n_row_tiles
        for j = 1 : g.n_col_tiles
            % calculate histogram
            h = lbp(g.tiled_img{i,j}, 1, 8, mapping, 'h');
            h = h / sum(h);
            histograms{i,j} = constructhf(h, mapping);
        end
    end