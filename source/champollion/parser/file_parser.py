# :coding: utf-8

import os

from .class_parser import get_class_environment
from .function_parser import get_function_environment
from .data_parser import get_data_environment


def get_file_environment(file_path, file_id, module_id, environment=None):
    """Return file environment from *file_path*.

    *file_id* represent the ID of the file.

    *module_id* represent the ID of the module.

    Update the *environment* is available and return it as-is if the file
    is not readable.

    Return dictionary in the form of::

        {
            "class": {...},
            "method": {...},
            "attribute": {...},
            "function": {...},
            "data": {...},
            "file": {
                "path/to/file.js": {
                    "id": "path/to/file.js",
                    "name": "script.js",
                    "path": "/path/to/script.js",
                    "content": "'use strict'\\n\\n..."
                },
                ...
            }
        }

    """
    if environment is None:
        environment = {}

    file_environment = {
        "id": file_id,
        "module_id": module_id,
        "name": os.path.basename(file_path),
        "path": file_path,
        "content": None,
        "class": {},
        "data": {},
        "function": {},
    }
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except (IOError, OSError):
        return environment

    file_environment["class"] = get_class_environment(content, module_id)
    file_environment["function"] = get_function_environment(content, module_id)
    file_environment["data"] = get_data_environment(content, module_id)
    file_environment["content"] = content

    method_environment = {}
    attribute_environment = {}

    # Extract methods and attributes from class environment to set it in the
    # top level environment.
    for _class in file_environment["class"].values():
        method_environment.update(_class["method"].copy())
        attribute_environment.update(_class["attribute"].copy())

    if "class" not in environment.keys():
        environment["class"] = {}
    environment["class"].update(file_environment["class"])

    if "method" not in environment.keys():
        environment["method"] = {}
    environment["method"].update(method_environment)

    if "attribute" not in environment.keys():
        environment["attribute"] = {}
    environment["attribute"].update(attribute_environment)

    if "function" not in environment.keys():
        environment["function"] = {}
    environment["function"].update(file_environment["function"])

    if "data" not in environment.keys():
        environment["data"] = {}
    environment["data"].update(file_environment["data"])

    if "file" not in environment.keys():
        environment["file"] = {}
    environment["file"][file_id] = file_environment

    return environment
