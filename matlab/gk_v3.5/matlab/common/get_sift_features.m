function [desc, hist] = get_sift_features(g, p)
    % get descriptor
    [f, d] = get_img_sift_descriptors(g.img, p);
    % plot feature positions
    if p.plot_wanted
        set(0, 'CurrentFigure', g.figures(3));
        plot(f(1,:), f(2,:), 'g*');
    end
    hist = cell(g.n_row_tiles, g.n_col_tiles);
    desc = cell(g.n_row_tiles, g.n_col_tiles);
    % traverse all nodes (tiles)
    for i = 1 : g.n_row_tiles
        min_max = g.row_boundaries{i};
        row_idxs = find(f(2,:)>=min_max(1) & f(2,:)<=min_max(2));
        for j = 1 : g.n_col_tiles
            % calculate average of all descriptors in this tile
            min_max = g.col_boundaries{j};
            col_idxs = find(f(1,:)>=min_max(1) & f(1,:)<=min_max(2));            
            hist{i,j} = mean(d(:,intersect(row_idxs,col_idxs)),2)';
            desc{i,j} = d(:,intersect(row_idxs,col_idxs))';
        end
    end