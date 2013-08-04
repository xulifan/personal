function img = read_standardized_img(fname, max_len)
    img = vl_imreadgray(fname);
    img = im2single(img);
    [height, width] = size(img);
    if (width > height)
        if width > max_len
            img = imresize(img, [NaN max_len]);
        end
    else
        if height > max_len
            img = imresize(img, [max_len NaN]);
        end
    end