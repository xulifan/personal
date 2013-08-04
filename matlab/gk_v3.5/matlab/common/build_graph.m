function graph = build_graph(filename, n_px, p)
    graph.filename = filename;
    graph.img = read_standardized_img(graph.filename, p.max_img_len);
    fprintf(1, 'LOG: image read: (%d, %d)\n', size(graph.img,1), size(graph.img,2));
    % create tiles and graph information
    [height, width] = size(graph.img);
    graph.tiled_img = mat2cell(graph.img, create_tile_sizes_px(height,n_px), create_tile_sizes_px(width,n_px));
    [graph.n_row_tiles, graph.n_col_tiles] = size(graph.tiled_img);
    % record tile boundaries
    graph.col_boundaries = cell(1, graph.n_row_tiles);
    graph.row_boundaries = cell(1, graph.n_col_tiles);
    start_idx = 1;
    for i = 1 : graph.n_row_tiles
        graph.row_boundaries{1,i} = [start_idx, start_idx+size(graph.tiled_img{i,1},1)-1];
        start_idx = start_idx + size(graph.tiled_img{i,1},1);
    end
    start_idx = 1;
    for i = 1 : graph.n_col_tiles
        graph.col_boundaries{1,i} = [start_idx, start_idx+size(graph.tiled_img{1,i},2)-1];
        start_idx = start_idx + size(graph.tiled_img{1,i},2);
    end
    % create figure
    if p.plot_wanted
        f3 = figure('Menubar', 'none'); clf;
        imshow(graph.img, 'InitialMagnification', 100, 'Border', 'tight'); hold on; axis image off;
        pos = get(f3, 'Position');
        pos(1:2) = [10, 600];
        set(f3, 'Position', pos);
        graph.figures = [0, 0, f3];
        print(f3, '-dpng', '~/Desktop/Data/test/c.png')
    end
    % apply the desired feature extractor CHANGE THIS TO JUST ONE CALL
    if strcmp(p.feat_type, 'LBP')
        [graph.descriptors, graph.histograms] = get_lbp_features(graph);
    elseif strcmp(p.feat_type, 'SIFT')
        [graph.descriptors, graph.histograms] = get_sift_features(graph, p);
    elseif strcmp(p.feat_type, 'COVDET')
        [graph.descriptors, graph.histograms] = get_sift_features(graph, p);
    end
    % show plots if wanted
    if p.plot_wanted
        f1 = figure('Menubar', 'none'); clf;
        pos = get(f1, 'Position');
        pos(1:2) = [10, 10];
        set(f1, 'Position', pos);        
        f2 = figure('Menubar', 'none'); clf;
        pos = get(f2, 'Position');
        pos(1:2) = [500, 500];
        set(f2, 'Position', pos);
        for i = 1 : graph.n_row_tiles
            for j = 1 : graph.n_col_tiles
                set(0, 'CurrentFigure', f1);          
                subplot(graph.n_row_tiles, graph.n_col_tiles, (i-1)*graph.n_col_tiles+j); imshow(graph.tiled_img{i,j},'InitialMagnification',100,'Border','tight'); axis image off;
                set(gca, 'LooseInset', get(gca,'TightInset'));
                set(0, 'CurrentFigure', f2);                
                subplot(graph.n_row_tiles, graph.n_col_tiles, (i-1)*graph.n_col_tiles+j); 
                plot(graph.histograms{i,j}); set(gca,'XTickLabel',''); axis tight;
                set(gca, 'LooseInset', get(gca,'TightInset'));
            end
        end
        graph.figures = [f1, f2, f3];
        print(f1, '-dpng', '~/Desktop/Data/test/a.png')
        print(f2, '-dpng', '~/Desktop/Data/test/b.png')
        
    end
    