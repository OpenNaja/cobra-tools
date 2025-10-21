import os


def to_import_path(folder: str) -> str:
    # convert a folder path like "cobra_core/generated" to an import path like "cobra_core.generated"
    # the folder can be a absolute path which should be normalized to a relative path based on CWD
    cwd = os.getcwd()
    return os.path.relpath(folder, cwd).replace(os.path.sep, '.')


def module_path_to_import_path(module_path: str, folder: str) -> str:
    return f"{folder}.{module_path}".replace(os.path.sep, '.')


def module_path_to_file_path(module_path: str, folder: str, root_dir: str, mkdir: bool = True) -> str:
    fp: str = os.path.join(root_dir, folder, module_path + ".py")
    if mkdir:
        fd: str = os.path.dirname(fp)
        if not os.path.isdir(fd):
            os.makedirs(fd)
    return fp

def pluralize_name(name: str) -> str:
    """Pluralizes a folder name by adding 's' unless it already ends with 's'."""
    return name if name.endswith('s') else f"{name}s"
