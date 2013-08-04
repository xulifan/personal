function histograms = find_sift_features(g, p)
    if strcmp(p.feat_type, 'SIFT')
        [f, d] = vl_sift(g.img);
    elseif strcmp(p.feat_type, 'PHOW');
        [f, d] = vl_phow(g.img);
    elseif strcmp(p.feat_type, 'COVDET');
        [f, d] = vl_covdet(g.img, 'EstimateOrientation', true);
        %[f, d] = vl_covdet(g.img,'Method', 'MultiscaleHessian', 'EstimateOrientation', true, 'EstimateAffineShape', true);
    end
    if p.plot_wanted
        set(0, 'CurrentFigure', g.figures(3));
        plot(f(1,:), f(2,:), 'g*');
    end
    histograms = cell(g.n_row_tiles, g.n_col_tiles);
    % traverse all nodes (tiles)
    for i = 1 : g.n_row_tiles
        min_max = g.row_boundaries{i};
        row_idxs = find(f(2,:)>=min_max(1) & f(2,:)<=min_max(2));
        for j = 1 : g.n_col_tiles
            % calculate average of all descriptors in this tile
            min_max = g.col_boundaries{j};
            col_idxs = find(f(1,:)>=min_max(1) & f(1,:)<=min_max(2));            
            histograms{i,j} = mean(d(:,intersect(row_idxs,col_idxs)),2)';                              
        end
    end