# :coding: utf-8


def get_module_environment(file_id, files, environment=None):
    """Return module ID and updated environment from *file_id*.

    *file_id* is in the form of::

        relative/path/to/file.js

    *files* is the list of files at the same level of the *file_id* analysed.

    Update the *environment* is available and return it as-is if the file
    is not readable.

    """
    if environment is None:
        environment = {
            "module": {}
        }

    hierarchy = file_id.split("/")
    file_name = hierarchy.pop()

    if file_name == "index.js":
        module_id = ".".join(hierarchy)
        module_name = guess_module_name(
            hierarchy[-1],
            hierarchy_folders=hierarchy[:-1],
            module_names=environment["module"].keys()
        )

    elif "index.js" in files:
        name = file_name.split(".js")[0]
        module_id = ".".join(hierarchy + [name])
        module_name = guess_module_name(
            ".".join([hierarchy[-1], name]),
            hierarchy_folders=hierarchy[:-1],
            module_names=environment["module"].keys()
        )

    else:
        name = file_name.split(".js")[0]
        module_id = ".".join(hierarchy + [name])
        module_name = name

    environment["module"][module_id] = {
        "id": module_id,
        "name": module_name,
        "file_id": file_id
    }

    return module_id, environment


def guess_module_name(name, hierarchy_folders, module_names):
    """Return the full module *name* from *hierarchy_folders*.

    *module_names* is the list of modules already recorded.

    """
    for i in range(len(hierarchy_folders)):
        root_module = ".".join(hierarchy_folders[i:])
        if root_module in module_names:
            return ".".join([root_module, name])

    return name
