% -------------------------------------------------------------------------
% plot image and descriptor
function visualize_descriptors
% -------------------------------------------------------------------------
close all;
% add software to path
run('~/s/vlfeat-0.9.16/toolbox/vl_setup');
% testing sift descriptors 
fname = 'ship.jpg';

% read images
I = im2single(rgb2gray(imread(fname)));
%J = rot90(I, floor(rand()*4));
J = imrotate(I, floor(rand()*360));
J = imresize(J, [NaN 200]);

% find descriptors 
[f, d] = vl_covdet(I, 'EstimateOrientation', true);
[f1, d1] = vl_covdet(J, 'EstimateOrientation', true);

% match images
plot_img_desc(I, f, d, J, f1, d1, 10);

% -------------------------------------------------------------------------
% plot image and descriptor
function plot_img_desc(im, f, d, im1, f1, d1, k)
% -------------------------------------------------------------------------
sep = 10;
img = zeros(max(size(im,1),size(im1,1)), size(im,2)+size(im1,2)+sep);
img(1:size(im,1), 1:size(im,2)) = im;
st_col = size(im,2) + sep + 1;
img(1:size(im1,1), st_col:st_col+size(im1,2)-1) = im1;
figure;
imshow(img);
hold on;
plot(f(1,:), f(2,:), 'o', 'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'g', 'MarkerSize', 7);
plot(f1(1,:)+st_col-1, f1(2,:), 'o', 'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'r', 'MarkerSize', 7);
[m, scores] = vl_ubcmatch(d, d1, 12);
for i = 1 : min(k, numel(scores))
    pos = f(1:2,m(1,i))';
    pos1 = f1(1:2,m(2,i))';
    line([pos(1),pos1(1)+st_col-1], [pos(2),pos1(2)], 'Color', [1,1,0]);
end
hold off;