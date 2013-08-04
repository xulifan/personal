function interesting = remove_nodes(g, p)
    if p.plot_wanted
        set(0, 'CurrentFigure', g.figures(3));
    end
    interesting = zeros(size(g.tiled_img));
    % mark interesting nodes
    for i = 1 : g.n_row_tiles
        mmr = g.row_boundaries{i};
        for j = 1 : g.n_col_tiles
            mmc = g.col_boundaries{j};
            if mean(mean(g.tiled_img{i,j})) > 0.175 && ~isnan(sum(g.histograms{i,j})) && sum(g.histograms{i,j}~=0) > 0
                interesting(i,j) = true;
                if p.plot_wanted                    
                    rectangle('Position', [mmc(1), mmr(1), mmc(2)-mmc(1), mmr(2)-mmr(1)], 'EdgeColor', [1, 1, 0], 'Curvature', [0.2, 0.2], 'LineWidth', 1.1);
                end
            else
                interesting(i,j) = false;
            end
        end
    end
    if p.plot_wanted
        set(0, 'CurrentFigure', g.figures(3));
        [~, ttt, ~] = fileparts(g.filename);
        title(ttt, 'Interpreter', 'none');
        hold off;
        print(g.figures(3), '-dpng', '~/Desktop/Data/test/d.png')
    end