function [pred, decv] = msvm_test(x, y, model)
	decv = zeros(size(y,1), model.n_models);
	for i = 1 : model.n_models
		[~,~,d] = svmpredict(double(strcmp(model.label_set{i},y)), x, model.models{i});
		decv(:,i) = d * (2 * model.models{i}.Label(1) - 1);
	end
	[~,pred] = max(decv, [], 2);
	pred = model.label_set(pred);