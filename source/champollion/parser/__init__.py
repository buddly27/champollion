# :coding: utf-8

"""Parser to fetch_environment all information from a :term:`Javascript` API in order
to document each element from a simple identifier.
"""

import os

from .js_module import fetch_environment as fetch_module_environment
from .js_file import fetch_environment as fetch_file_environment


def fetch_environment(path):
    """Return :term:`Javascript` environment dictionary from *path* structure.

    Raises :exc:`OSError` if the directory is incorrect.

    The environment is in the form of::

        {
            "module": {
                "module.id": {
                    "id": "module.id",
                    "name": "module_name",
                    "file_id": "file/id/index.js"
                    "description": "A module."
                    ...
                },
                ...
            },
            "file": {
                "file/id/index.js": {
                    "id": "file/id/index.js",
                    "module_id": "module_id",
                    "content": "...",
                    ...
                },
                ...
            },
            "class": {
                "class_id": {
                    "id": "class_id",
                    "module_id": "module_id"
                    "description": "A class."
                    ...
                },
                ...
            },
            "method": {
                "method_id": {
                    "id": "method_id",
                    "class_id": "class_id",
                    "module_id": "module_id",
                    "description": "A method."
                    ...
                },
                ...
            },
            "attribute": {
                "attribute_id": {
                    "id": "attribute_id",
                    "class_id": "class_id",
                    "module_id": "module_id",
                    "description": "An attribute."
                    ...
                },
                ...
            },
            "function": {
                "function_id": {
                    "id": "function_id",
                    "module_id": "module_id",
                    "description": "A function."
                    ...
                },
                ...
            },
            "data": {
                "data_id": {
                    "id": "data_id",
                    "module_id": "module_id",
                    "description": "A variable."
                    ...
                },
                ...
            }
        }

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

            # Fetch module environment
            _module_environment = fetch_module_environment(
                file_id, files, module_names=[
                    _module["name"] for _module in
                    environment["module"].values()
                ]
            )
            module_id = _module_environment["id"]
            environment["module"][module_id] = _module_environment

            # Fetch file environment
            _file_environment = fetch_file_environment(
                file_path, file_id, _module_environment["id"]
            )
            file_id = _file_environment["id"]

            method_environment = {}
            attribute_environment = {}

            # Extract methods and attributes from class environment to set it
            # in the top level environment.
            for _class in _file_environment["class"].values():
                method_environment.update(_class["method"].copy())
                attribute_environment.update(_class["attribute"].copy())

            environment["file"][file_id] = _file_environment
            environment["function"].update(_file_environment["function"])
            environment["data"].update(_file_environment["data"])
            environment["class"].update(_file_environment["class"])
            environment["method"].update(method_environment)
            environment["attribute"].update(attribute_environment)

    return environment
