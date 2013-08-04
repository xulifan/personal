function [sizes] = create_tile_sizes_px(side_length, n_px)
    if side_length < n_px
        error('lenght of this side (%d) cannot be shorter than n_px (%d)',side_length,n_px);
    end
    n_tiles = floor(side_length/n_px);
    sizes = ones(1, n_tiles) * floor(side_length/n_tiles);
    sizes(1:mod(side_length,n_tiles)) = sizes(1:mod(side_length,n_tiles)) + 1;
    if sum(sizes) ~= side_length
        error('bin-size calculation error');
    end
