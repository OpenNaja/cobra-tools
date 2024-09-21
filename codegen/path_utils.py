import os


def to_import_path(folder):
    # convert a folder path like "cobra_core/generated" to an import path like "cobra_core.generated"
    # the folder can be a absolute path which should be normalized to a relative path based on CWD
    cwd = os.getcwd()
    return os.path.relpath(folder, cwd).replace(os.path.sep, '.')


def module_path_to_import_path(module_path, folder):
    return f"{folder}.{module_path}".replace(os.path.sep, '.')


def module_path_to_file_path(module_path, folder, root_dir, mkdir=True):
    fp = os.path.join(root_dir, folder, module_path + ".py")
    if mkdir:
        fd = os.path.dirname(fp)
        if not os.path.isdir(fd):
            os.makedirs(fd)
    return fp
