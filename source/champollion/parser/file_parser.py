# :coding: utf-8

import os

from .class_parser import get_class_environment
from .function_parser import get_function_environment
from .data_parser import get_data_environment
from .helper import get_import_environment, get_export_environment


def get_file_environment(file_path, file_id, module_id, environment=None):
    """Return file environment from *file_path*.

    *file_id* represent the ID of the file.

    *module_id* represent the ID of the module.

    Update the *environment* if available and return it as-is if the file
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
        "export": {},
        "import": {}
    }
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except (IOError, OSError):
        return environment

    export_environment = get_export_environment(content, module_id)

    for _env_id, _env in get_class_environment(content, module_id).items():
        _update_environment_from_exported_elements(_env, export_environment)
        file_environment["class"][_env_id] = _env

    for _env_id, _env in get_function_environment(content, module_id).items():
        _update_environment_from_exported_elements(_env, export_environment)
        file_environment["function"][_env_id] = _env

    for _env_id, _env in get_data_environment(content, module_id).items():
        _update_environment_from_exported_elements(_env, export_environment)
        file_environment["data"][_env_id] = _env

    file_environment["import"] = get_import_environment(content, module_id)

    file_environment["export"] = export_environment
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


def _update_environment_from_exported_elements(environment, export_environment):
    """Update *environment* with exported elements from *export_environment*.

    For instance, the element environment might not be exported, but an
    exported element is found that can be linked to this element.

    .. code-block:: js

        # Element is the environment
        function doSomething(arg1, arg2) {
            console.log("Hello World")
        }

        # Element in the export environment
        export {doSomething};

    In the example above, the function `doSomething` is previously fetched
    without the exported attribute, so it will be added to it.

    The entry will then be removed from the *export_environment*.

    .. warning::

        Both input environments are mutated.

    """
    env_id = environment["id"]

    # Update the environment from exported environment if necessary
    if env_id in export_environment.keys() and not environment["exported"]:
        expression_environment = export_environment[env_id]

        environment["exported"] = True
        environment["default"] = expression_environment["default"]

        if environment["description"] is None:
            environment["description"] = (
                expression_environment["description"]
            )

        # Once the environment is updated, we can remove the key from the
        # exported environment to prevent displaying it twice.
        del export_environment[env_id]
