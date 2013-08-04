function model = msvm_train(x, y, label_set, len, options)
	models = cell(len, 1);
	for i = 1 : len
		models{i} = svmtrain(double(strcmp(y,label_set(i))), x, options);
	end
	model.models = models;
	model.label_set = label_set;
	model.n_models = len;