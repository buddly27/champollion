# :coding: utf-8

import os
import re

from .js_class import fetch_environment as fetch_class_environment
from .js_function import fetch_environment as fetch_function_environment
from .js_data import fetch_environment as fetch_data_environment

from .helper import get_docstring, filter_comments


#: Regular Expression pattern for imported element
_IMPORTED_ELEMENT_PATTERN = re.compile(
    r"(?P<start_regex>(\n|^)) *import +"
    r"(?P<expression>({([^{}]|\n)+}|.+))"
    r" +from +['\"](?P<module>[\w/.\\_-]+)['\"];?"
)

#: Regular Expression pattern for exported element
_EXPORTED_ELEMENT_PATTERN = re.compile(
    r"(?P<start_regex>(\n|^)) *export +(?P<default>default +)?"
    r"((?P<expression_from_module>({([^{}]|\n)+}|.+))"
    r" +from +['\"](?P<module>[\w/.\\_-]+)['\"]|"
    r"(?P<expression_from_variable>({([^{}]|\n)+}|.+)));?"
)

#: Regular Expression pattern for binding element
_BINDING_ELEMENT_PATTERN = re.compile(
    r"^(?P<name>(\w+|\*))( +as +(?P<alias>\w+))?;?$"
)

#: Regular Expression pattern for file docstring
_FILE_DOCSTRING_PATTERN = re.compile(r"^/\*\*.*?\*/(?=\n\n)", re.DOTALL)


def fetch_environment(file_path, file_id, module_id):
    """Return file environment dictionary from *file_path*.

    *file_id* represent the identifier of the file.

    *module_id* represent the identifier of the module.

    Update the *environment* if available and return it as-is if the file
    is not readable.

    The environment is in the form of::

        {
            "id": "module/test/index.js",
            "module_id": "module.test",
            "name": "index.js",
            "path": "/path/to/module/test/index.js",
            "content": "'use strict'\\n\\n...",
            "description": "File description",
            "export": {
                "module.test.exported_element": {
                    "id": "module.test.exported_element",
                    "module": "module.test.from_module",
                    "description": "An exported element",
                    ...
                },
                ...
            },
            "import": {
                "module.test.imported_element": {
                    "id": "module.test.imported_element",
                    "module": "module.test.from_module",
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
            "data": {
                "data_id": {
                    "id": "data_id",
                    "module_id": "module_id",
                    "description": "A variable."
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
            }
        }

    """
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except (IOError, OSError):
        return

    environment = {
        "id": file_id,
        "module_id": module_id,
        "name": os.path.basename(file_path),
        "path": file_path,
        "content": content,
        "description": fetch_file_description(content),
        "export": fetch_export_environment(content, module_id),
        "import": fetch_import_environment(content, module_id),
        "class": {},
        "data": {},
        "function": {}
    }

    for _env_id, _env in fetch_class_environment(content, module_id).items():
        update_from_exported_elements(_env, environment["export"])
        environment["class"][_env_id] = _env

    for _env_id, _env in fetch_function_environment(content, module_id).items():
        update_from_exported_elements(_env, environment["export"])
        environment["function"][_env_id] = _env

    for _env_id, _env in fetch_data_environment(content, module_id).items():
        update_from_exported_elements(_env, environment["export"])
        environment["data"][_env_id] = _env

    return environment


def fetch_file_description(content):
    """Return file description from *content*.

    The description must be in a docstring which should be defined at the very
    beginning of the file. It can only be preceded by one line comments.

    It must be in the form of::

        /**
         * File description.
         *
         * A detailed description of the file.
         *
         */

    Return None if no description is available.

    """
    content = filter_comments(content, filter_multiline_comment=False).strip()

    match = _FILE_DOCSTRING_PATTERN.search(content)
    if match is None:
        return

    docstring_content = match.group()[3:-2].strip()

    # If the entire docstring fit in one line
    if match.group().count("\n") == 0:
        return docstring_content

    docstring = []

    for line in docstring_content.split("\n"):
        line = line.strip()

        # Valid docstring line starts with a '*'
        if re.search("^\*( *| +.+)$", line) is not None:
            indentation = 2 if len(line) > 1 else 1
            docstring.append(line[indentation:].rstrip())

        # Error in the docstring
        else:
            return

    return "\n".join(docstring)


def update_from_exported_elements(environment, export_environment):
    """Update *environment* with exported elements from *export_environment*.

    For instance, the element environment might not be exported, but an
    exported element is found that can be linked to this element.

    .. code-block:: js

        // Element in the environment
        function doSomething(arg1, arg2) {
            console.log("Hello World")
        }

        // Element in the export environment
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


def fetch_import_environment(content, module_id):
    """Return import environment dictionary from *content*.

    *module_id* represent the identifier of the module.

    The environment is in the form of::

        {
            "module.test.imported_element": {
                "id": "module.test.imported_element",
                "module": "module.test.from_module",
                "name": "imported_element",
                "alias": None,
                "partial": False
            },
            ...
        }

    """
    environment = {}

    wildcards_number = 0

    module_path = module_id.replace(".", os.sep)

    for match in _IMPORTED_ELEMENT_PATTERN.finditer(content):
        from_module_path = os.path.normpath(
            os.path.join(module_path, match.group("module"))
        )
        from_module_id = from_module_path.replace(os.sep, ".")

        element_raw = match.group("expression").replace("\n", "")

        _env, wildcards_number = _fetch_expression_environment(
            element_raw, module_id, from_module_id,
            wildcards_number=wildcards_number,
            environment=environment
        )
        environment.update(_env)

    return environment


def fetch_export_environment(content, module_id):
    """Return export environment dictionary from *content*.

    *module_id* represent the identifier of the module.

    The environment is in the form of::

        {
            "module.test.exported_element": {
                "id": "module.test.exported_element",
                "module": "module.test.from_module",
                "name": "exported_element",
                "alias": None,
                "partial": True,
                "description": None,
                "default": False,
                "line_number": 5,
            },
            ...
        }

    """
    environment = {}

    wildcards_number = 0

    lines = content.split("\n")

    module_path = module_id.replace(".", os.sep)

    for match in _EXPORTED_ELEMENT_PATTERN.finditer(content):
        line_number = (
            content[:match.start()].count("\n") +
            match.group("start_regex").count("\n") + 1
        )

        from_module_id = None

        if match.group("module") is not None:
            from_module_path = os.path.normpath(
                os.path.join(module_path, match.group("module"))
            )
            from_module_id = from_module_path.replace(os.sep, ".")

        expression = match.group("expression_from_variable")
        if expression is None:
            expression = match.group("expression_from_module")

        element_raw = expression.replace("\n", "")

        _env, wildcards_number = _fetch_expression_environment(
            element_raw, module_id, from_module_id,
            wildcards_number=wildcards_number,
        )

        for _env_id, _sub_env in _env.items():
            environment[_env_id] = {
                "description": get_docstring(line_number, lines),
                "line_number": line_number,
                "default": match.group("default") is not None,
            }
            environment[_env_id].update(_sub_env)

    return environment


def _fetch_expression_environment(
    expression, module_id, from_module_id=None, environment=None,
    wildcards_number=0
):
    """Return tuple with *expression* environment and updated *wildcards_number*.

    *module_id* represent the identifier of the module.

    *from_module_id* is the optional module identifier from which the
    expression can be resolved.

    Update the *environment* if available and return it as-is if the file
    is not readable.

    *wildcards_number* represent the number of `*` found as un-aliased binding.

    """
    if environment is None:
        environment = {}

    # Parse partial expressions first
    for partial_match in re.finditer("{[^{}]+}", expression):
        binding_environments, wildcards_number = _fetch_binding_environment(
            partial_match.group()[1:-1], module_id, wildcards_number
        )
        for _env in binding_environments:
            element_id = _env["id"]
            environment[element_id] = _env
            environment[element_id].update(
                {"partial": True, "module": from_module_id}
            )

        # remove partial imports from expression
        expression = (
            expression[:partial_match.start()] +
            " " * len(partial_match.group()) +
            expression[partial_match.end():]
        )

    # Then parse the default expressions
    binding_environments, wildcards_number = _fetch_binding_environment(
        expression, module_id, wildcards_number
    )
    for _env in binding_environments:
        element_id = _env["id"]
        environment[element_id] = _env
        environment[element_id].update(
            {"partial": False, "module": from_module_id}
        )

    return environment, wildcards_number


def _fetch_binding_environment(expression, module_id, wildcards_number=0):
    """Return tuple with list of binding environments from *expression* and
    updated *wildcards_number*.

    *module_id* represent the identifier of the module.

    *wildcards_number* represent the number of `*` found as un-aliased binding.

    Example::

        expression = "Module1 as ModuleAlias, Module2"
        env = get_import_module_environment(expression, "test.module")

    The result would be::

        {
            "test.module.ModuleAlias": {
                "id": "test.module.ModuleAlias",
                "name": "Module1",
                "alias": "ModuleAlias"
            },
            "test.module.Module2": {
                "id": "test.module.ModuleAlias",
                "name": "Module2",
                "alias": None
            }
        }

    """
    environments = []

    for element in expression.split(","):
        _element = element.strip()
        if len(_element) == 0:
            continue

        match = _BINDING_ELEMENT_PATTERN.match(_element)
        if match is None:
            continue

        name = match.group("name")
        alias = match.group("alias")

        # Determine element ID if an alias is set
        element_id = alias if alias is not None else name
        if element_id == "*":
            wildcards_number += 1
            element_id = "WILDCARD_{0}".format(wildcards_number)

        element_id = "{module}.{id}".format(
            module=module_id, id=element_id
        )

        _module = {
            "id": element_id,
            "name": name,
            "alias": alias
        }
        environments.append(_module)

    return environments, wildcards_number
