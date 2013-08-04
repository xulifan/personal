function [f, d] = get_img_sift_descriptors(img, p)
    if strcmp(p.feat_type, 'SIFT')
        [f, d] = vl_sift(img);
    elseif strcmp(p.feat_type, 'COVDET');
        [f, d] = vl_covdet(img, 'EstimateOrientation', true);
    elseif strcmp(p.feat_type, 'PHOW');
        [f, d] = vl_dsift(img);
    end
    if p.normalize_descriptor
        aux = repmat(sum(d),size(d,1),1);
        d = double(d) ./ aux;
    end