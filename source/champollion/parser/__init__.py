# :coding: utf-8

import os

from .module_parser import get_module_environment
from .file_parser import get_file_environment


def get_environment(path):
    """Return javascript environment dictionary from *path*.

    Analyse the content of *path* recursively.

    Raises :exc:`OSError` if the directory is incorrect.

    """
    if not os.path.isdir(path) or not os.access(path, os.R_OK):
        raise OSError(
            "The javascript package directory is incorrect: {0}".format(path)
        )

    environment = {
        "module": {},
        "class": {},
        "method": {},
        "attribute": {},
        "function": {},
        "data": {},
        "file": {}
    }

    repository_name = os.path.basename(path)

    extensions = [".js", ".jsx"]

    for root, dirs, files in os.walk(path):
        root_folders = (
            [repository_name] + root.split(path)[-1].split(os.sep)[1:]
        )

        files[:] = [
            f for f in files
            if os.path.splitext(f)[1] in extensions
            and not f.startswith(".")
        ]

        dirs[:] = [
            d for d in dirs
            if not d.startswith(".")
        ]

        for _file in files:
            file_id = "/".join(root_folders + [_file])
            file_path = os.path.join(root, _file)

            module_id, environment = get_module_environment(
                file_id, files, environment
            )

            environment = get_file_environment(
                file_path, file_id, module_id, environment
            )

    return environment
