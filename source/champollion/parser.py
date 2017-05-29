# :coding: utf-8

import os
import re

#: Regular Expression pattern for single line comments
ONE_LINE_COMMENT_PATTERN = re.compile(r"//.*?\n")

#: Regular Expression pattern for multi-line comments
MULTI_LINES_COMMENT_PATTERN = re.compile(r"/\*(.|\n)*?\*/")

#: Regular Expression pattern for classes
CLASS_PATTERN = re.compile(
    r"(?P<export>export +)?(?P<default>default +)?"
    r"(class +(?P<class_name>\w+)|const +(?P<variable_name>\w+) *= *class +\w+)"
    r"( +extends +(?P<mother_class>\w+))? *{"
)

#: Regular Expression pattern for function expressions
FUNCTION_PATTERN = re.compile(
    r"(?P<export>export +)?(?P<default>default +)?"
    r"function (?P<function_name>\w+) *\((?P<arguments>.*)\) *{"
)

#: Regular Expression pattern for arrow functions
FUNCTION_ARROW_PATTERN = re.compile(
    r"(?P<export>export +)?(?P<default>default +)?"
    r"const (?P<function_name>\w+) *= *\((?P<arguments>.*)\) *=> *{"
)

#: Regular Expression pattern for variables
VARIABLES_PATTERN = re.compile(
    r"(?P<export>export +)?(?P<default>default +)?"
    r"(?P<variable_type>(const|let|var)) (?P<variable_name>\w+) "
    r"*= *(?P<variable_value>[^;]+);"
)


def get_environment(path):
    """Return javascript environment dictionary from *path*.

    Analyse the content of *path* recursively.

    Raises :exc:`OSError` if the directory is incorrect.

    """
    if not os.path.isdir(path) or not os.access(path, os.R_OK):
        raise OSError(
            "The javascript package directory is incorrect: {0}".format(path)
        )

    environment = dict(
        modules={},
        classes={},
        functions={},
        variables={},
        files={}
    )

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
            "modules": {}
        }

    hierarchy = file_id.split("/")
    file_name = hierarchy.pop()

    if file_name == "index.js":
        module_id = ".".join(hierarchy)
        module_name = guess_module_name(
            hierarchy[-1],
            hierarchy_folders=hierarchy[:-1],
            module_names=environment["modules"].keys()
        )

    elif "index.js" in files:
        name = file_name.split(".js")[0]
        module_id = ".".join(hierarchy + [name])
        module_name = guess_module_name(
            ".".join([hierarchy[-1], name]),
            hierarchy_folders=hierarchy[:-1],
            module_names=environment["modules"].keys()
        )

    else:
        name = file_name.split(".js")[0]
        module_id = ".".join(hierarchy + [name])
        module_name = name

    environment["modules"][module_id] = dict(
        id=module_id,
        name=module_name,
        file_id=file_id
    )

    return module_id, environment


def get_file_environment(file_path, file_id, module_id, environment=None):
    """Return file environment from *file_path*.

    *file_id* represent the ID of the file.

    *module_id* represent the ID of the module.

    Update the *environment* is available and return it as-is if the file
    is not readable.

    Otherwise return dictionary in the form of::

        {
            "classes": {...},
            "functions": {...},
            "variables": {...},
            "files": {
                "path/to/file.js": {
                    "id": "path/to/file.js",
                    "name": "script.js",
                    "path": "/path/to/script.js",
                    "content": "'use strict'\\n\\n...",
                    "classes": [
                        ...
                    ],
                    "functions": [
                        ...
                    ]
                    "variables": [
                        ...
                    ]

                },
                ...
            }
        }

    """
    if environment is None:
        environment = {}

    file_environment = dict(
        id=file_id,
        module_id=module_id,
        name=os.path.basename(file_path),
        path=file_path,
        content=None,
        classes={},
        functions={},
        variables={},
    )
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except (IOError, OSError):
        return environment

    classes = get_class_environment(content, module_id)
    functions = get_function_environment(content, module_id)
    variables = get_variable_environment(content, module_id)

    file_environment["classes"] = classes.keys()
    file_environment["functions"] = functions.keys()
    file_environment["variables"] = variables.keys()
    file_environment["content"] = content

    if "classes" not in environment.keys():
        environment["classes"] = {}
    environment["classes"].update(classes)

    if "functions" not in environment.keys():
        environment["functions"] = {}
    environment["functions"].update(functions)

    if "variables" not in environment.keys():
        environment["variables"] = {}
    environment["variables"].update(variables)

    if "files" not in environment.keys():
        environment["files"] = {}
    environment["files"][file_id] = file_environment

    return environment


def get_class_environment(content, module_id):
    """Return class environment from *content*.

    *module_id* represent the ID of the module.

    Return dictionary in the form of::

        {
            "module.AwesomeClass": {
                "id": "module.AwesomeClass",
                "name": "AwesomeClass",
                "parent": "MotherClass",
                "line": 42,
                "description": "Class doc.\\n\\nDetailed description."
            },
            "module.another.SuperClass": {
                ...
            },
            ...
        }

    """
    environment = dict()

    lines = content.split("\n")
    content = filter_comments(content)
    content = collapse_all(content)

    for match in CLASS_PATTERN.finditer(content):
        class_name = match.group("class_name")
        if class_name is None:
            class_name = match.group("variable_name")

        class_id = ".".join([module_id, class_name])
        line_number = content[:match.start()].count("\n")+1

        class_environment = dict(
            id=class_id,
            module_id=module_id,
            exported=match.group("export") is not None,
            default=match.group("default") is not None,
            name=class_name,
            parent=match.group("mother_class"),
            line=line_number,
            description=get_docstring(line_number, lines)
        )
        environment[class_id] = class_environment

    return environment


def get_function_environment(content, module_id):
    """Return function environment from *content*.

    *module_id* represent the ID of the module.

    """
    environment = dict()

    lines = content.split("\n")
    content = filter_comments(content)
    content = collapse_all(content)

    for match_iter in (
        FUNCTION_ARROW_PATTERN.finditer(content),
        FUNCTION_PATTERN.finditer(content)
    ):
        for match in match_iter:
            function_id = ".".join([module_id, match.group("function_name")])
            line_number = content[:match.start()].count("\n")+1
            arguments = filter(lambda x: len(x), [
                arg.strip() for arg in match.group("arguments").split(",")
            ])

            function_environment = dict(
                id=function_id,
                module_id=module_id,
                exported=match.group("export") is not None,
                default=match.group("default") is not None,
                name=match.group("function_name"),
                arguments=arguments,
                line=line_number,
                description=get_docstring(line_number, lines)
            )
            environment[function_id] = function_environment

    return environment


def get_variable_environment(content, module_id):
    """Return variable environment from *content*.

    *module_id* represent the ID of the module.

    """
    environment = dict()

    lines = content.split("\n")
    content = filter_comments(content)
    content = collapse_all(content)

    for match in VARIABLES_PATTERN.finditer(content):
        variable_id = ".".join([module_id, match.group("variable_name")])
        line_number = content[:match.start()].count("\n")+1

        # As we collapsed all contexts to avoid noises, we need to get the
        # value from the original data in case it represents an object.
        match_in_line = VARIABLES_PATTERN.search(
            "\n".join(lines[line_number-1:])
        )

        variable_environment = dict(
            id=variable_id,
            module_id=module_id,
            exported=match.group("export") is not None,
            default=match.group("default") is not None,
            name=match.group("variable_name"),
            value=match_in_line.group("variable_value"),
            type=match.group("variable_type"),
            line=line_number,
            description=get_docstring(line_number, lines)
        )
        environment[variable_id] = variable_environment

    return environment


def get_docstring(line_number, lines):
    """Return docstrings for an element at a specific *line_number*.

    Loop into the file *lines* in reverse, starting from the element's
    *line_number* in order to parse the docstring if available.

    The docstring must be in the form of::

        /**
         * Class doc.
         *
         * Detailed description.
         */
        class AwesomeClass {
           ...
        }

    Which will return the following result::

        "Class doc.\\n\\nDetailed description."

    The docstring can also fit on one line, in the form of::

        /** Class doc. */
        class AwesomeClass {
           ...
        }

    """
    docstring = None

    for index in reversed(range(line_number-1)):
        line = lines[index].strip()
        if len(line) == 0:
            continue

        # Start of the docstring (from the end)
        if docstring is None:
            # If the entire docstring fit in one line
            match = re.search("(?<=/\*\* ).*(?= \*/)", line)
            if match is not None:
                return match.group()

            # No docstring
            if not line.startswith("*/"):
                return

            docstring = []

        # Valid docstring line starts with a '*'
        elif re.search("^\*( *| +.+)$", line) is not None:
            index = 2 if len(line) > 1 else 1
            docstring.append(line[index:].rstrip())

        # Beginning of valid docstrings starts with '/**'
        elif line.startswith("/**"):
            return "\n".join(docstring[::-1])

        # Error in the docstring
        else:
            return


def filter_comments(content):
    """Return *content* without the comments.

    .. note::

        The line numbers are preserved.

    """
    def _replace_comment(element):
        count = element.group().count("\n")
        return "\n" * count

    content = ONE_LINE_COMMENT_PATTERN.sub(_replace_comment, content)
    content = MULTI_LINES_COMMENT_PATTERN.sub(_replace_comment, content)

    return content


def collapse_all(content):
    """Return *content* with the top level elements only.

    .. note::

        The line numbers are preserved.

    """
    def _replace_comment(element):
        count = element.group().count("\n")
        return "<>{0}".format("\n" * count)

    _content = None

    while _content != content:
        _content = content
        content = re.sub(r"{[^{}]*}", _replace_comment, content)

    return content.replace("<>", "{}")


def guess_module_name(name, hierarchy_folders, module_names):
    """Return the full module *name* from *hierarchy_folders*.

    *module_names* is the list of modules already recorded.

    """
    for i in range(len(hierarchy_folders)):
        root_module = ".".join(hierarchy_folders[i:])
        if root_module in module_names:
            return ".".join([root_module, name])

    return name
