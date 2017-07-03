# :coding: utf-8


def fetch_environment(file_id, files=None, module_names=None):
    """Return module environment dictionary from *file_id*.

    *file_id* represent the identifier of the file.

    *files* is an optional list of the other file names stored in the same
    directory as the one analyzed.

    *module_names* is an optional list of all the other module name
    previously fetched to help determine the module name of the current
    file.

    The environment is in the form of::

        {
            "id": "module.test",
            "name": test,
            "file_id": "module/test/index.js"
        }

    """
    if module_names is None:
        module_names = []

    hierarchy = file_id.split("/")
    file_name = hierarchy.pop()

    if file_name == "index.js":
        module_id = ".".join(hierarchy)
        module_name = _guess_module_name(
            hierarchy[-1],
            hierarchy_folders=hierarchy[:-1],
            module_names=module_names
        )

    elif "index.js" in files:
        name = file_name.split(".js")[0]
        module_id = ".".join(hierarchy + [name])
        module_name = _guess_module_name(
            ".".join([hierarchy[-1], name]),
            hierarchy_folders=hierarchy[:-1],
            module_names=module_names
        )

    else:
        name = file_name.split(".js")[0]
        module_id = ".".join(hierarchy + [name])
        module_name = name

    return {
        "id": module_id,
        "name": module_name,
        "path": module_id.replace(".", "/"),
        "file_id": file_id
    }


def _guess_module_name(name, hierarchy_folders, module_names):
    """Return the full module *name* from *hierarchy_folders*.

    *module_names* is the list of modules already fetched.

    """
    for i in range(len(hierarchy_folders)):
        root_module = ".".join(hierarchy_folders[i:])
        if root_module in module_names:
            return ".".join([root_module, name])

    return name
