import os


def module_path_to_import_path(module_path, folder):
    return f"{folder}.{module_path.replace(os.path.sep, '.')}"


def module_path_to_output_file_path(module_path, folder, root_dir):
    # get the module path from the path of the file
    out_file = os.path.join(root_dir, folder, module_path + ".py")
    out_dir = os.path.dirname(out_file)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    return out_file
