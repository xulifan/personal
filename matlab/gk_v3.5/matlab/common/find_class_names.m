function classes = find_class_names(folder)
    classes = dir(folder);
    classes = classes([classes.isdir]);
    classes = {classes(3:end).name};