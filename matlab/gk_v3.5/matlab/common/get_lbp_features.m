function [desc, hist] = get_lbp_features(g)
    % prepare for applying LBP
    mapping = getmaplbphf(8);
    hist = cell(g.n_row_tiles, g.n_col_tiles);
    desc = {};
    % traverse all nodes (tiles)
    for i = 1 : g.n_row_tiles
        for j = 1 : g.n_col_tiles
            % calculate histogram
            h = lbp(g.tiled_img{i,j}, 1, 8, mapping, 'h');
            h = h / sum(h);
            hist{i,j} = constructhf(h, mapping);
        end
    end