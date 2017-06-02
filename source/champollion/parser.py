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
    r"(class +(?P<class_name>\w+)|const +(?P<data_name>\w+) *= *class +\w+)"
    r"( +extends +(?P<mother_class>[\w._-]+))? *{"
)

#: Regular Expression pattern for class methods
CLASS_METHOD_PATTERN = re.compile(
    r"(?P<prefix>(static|get|set) +)?"
    r"(?P<method_name>\w+) *\((?P<arguments>.*)\) *{"
)

#: Regular Expression pattern for class arrow methods
CLASS_METHOD_ARROW_PATTERN = re.compile(
    r"(?P<prefix>(static|get|set) +)?"
    r"(?P<method_name>\w+) *= *\((?P<arguments>.*)\) *=> *{"
)

#: Regular Expression pattern for class attribute
CLASS_ATTRIBUTE_PATTERN = re.compile(
    r"(?P<prefix>static +)?(?P<attribute_name>\w+) "
    r"*= *(?P<attribute_value>[^;>]+);"
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

#: Regular Expression pattern for data
DATA_PATTERN = re.compile(
    r"(?P<export>export +)?(?P<default>default +)?"
    r"(?P<data_type>(const|let|var)) (?P<data_name>\w+) "
    r"*= *(?P<data_value>[^;]+);"
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
        "content": None
    }
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except (IOError, OSError):
        return environment

    class_environment = get_class_environment(content, module_id)

    method_environment = {}
    attribute_environment = {}

    # Extract methods and attributes from class environment to set it in the
    # top level environment.
    for _class in class_environment.values():
        method_environment.update(_class["method"].copy())
        attribute_environment.update(_class["attribute"].copy())

    function_environment = get_function_environment(content, module_id)
    data_environment = get_data_environment(content, module_id)

    file_environment["content"] = content

    if "class" not in environment.keys():
        environment["class"] = {}
    environment["class"].update(class_environment)

    if "method" not in environment.keys():
        environment["method"] = {}
    environment["method"].update(method_environment)

    if "attribute" not in environment.keys():
        environment["attribute"] = {}
    environment["attribute"].update(attribute_environment)

    if "function" not in environment.keys():
        environment["function"] = {}
    environment["function"].update(function_environment)

    if "data" not in environment.keys():
        environment["data"] = {}
    environment["data"].update(data_environment)

    if "file" not in environment.keys():
        environment["file"] = {}
    environment["file"][file_id] = file_environment

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
    environment = {}

    lines = content.split("\n")

    # The comment filter is made during the collapse content process to
    # preserve the class content with all comments (and docstrings!)
    content, collapsed_content = collapse_all(content, filter_comment=True)

    for match in CLASS_PATTERN.finditer(content):
        class_name = match.group("class_name")
        if class_name is None:
            class_name = match.group("data_name")

        class_id = ".".join([module_id, class_name])
        line_number = content[:match.start()].count("\n")+1

        method_environment = {}
        attribute_environment = {}

        if line_number in collapsed_content.keys():
            class_content = collapsed_content[line_number][1:-1]

            method_environment = get_class_methods_environment(
                class_content, class_id, line_number=line_number-1
            )
            attribute_environment = get_class_attribute_environment(
                class_content, class_id, line_number=line_number-1
            )

        class_environment = {
            "id": class_id,
            "module_id": module_id,
            "exported": match.group("export") is not None,
            "default": match.group("default") is not None,
            "name": class_name,
            "parent": match.group("mother_class"),
            "line_number": line_number,
            "description": get_docstring(line_number, lines),
            "method": method_environment,
            "attribute": attribute_environment
        }
        environment[class_id] = class_environment

    return environment


def get_class_methods_environment(content, class_id, line_number=0):
    """Return function environment from *content*.

    *class_id* represent the ID of the class.

    *line_number* is the first line number of content

    """
    environment = {}

    lines = content.split("\n")
    content = filter_comments(content)
    content = collapse_all(content)[0]

    for match_iter in (
        CLASS_METHOD_ARROW_PATTERN.finditer(content),
        CLASS_METHOD_PATTERN.finditer(content)
    ):
        for match in match_iter:
            method_id = ".".join([class_id, match.group("method_name")])
            prefix = match.group("prefix")
            if prefix is not None:
                prefix = prefix.strip()

                # Add the prefix to the method ID if the method if a getter or
                # a setter as several method could have the same name.
                if prefix in ["get", "set"]:
                    method_id += "." + prefix

            _line_number = content[:match.start()].count("\n")+1
            arguments = filter(lambda x: len(x), [
                arg.strip() for arg in match.group("arguments").split(",")
            ])

            method_environment = {
                "id": method_id,
                "class_id": class_id,
                "module_id": class_id.rsplit(".", 1)[0],
                "name": match.group("method_name"),
                "prefix": prefix,
                "arguments": arguments,
                "line_number": _line_number+line_number,
                "description": get_docstring(_line_number, lines)
            }
            environment[method_id] = method_environment

    return environment


def get_class_attribute_environment(content, class_id, line_number=0):
    """Return function environment from *content*.

    *class_id* represent the ID of the class.

    *line_number* is the first line number of content

    """
    environment = {}

    lines = content.split("\n")
    content = filter_comments(content)
    content = collapse_all(content)[0]

    for match in CLASS_ATTRIBUTE_PATTERN.finditer(content):
        attribute_id = ".".join([class_id, match.group("attribute_name")])
        prefix = match.group("prefix")
        if prefix is not None:
            prefix = prefix.strip()

        _line_number = content[:match.start()].count("\n")+1

        # As we collapsed all contexts to avoid noises, we need to get the
        # value from the original data in case it represents an object.
        match_in_line = CLASS_ATTRIBUTE_PATTERN.search(
            "\n".join(lines[_line_number-1:])
        )

        attribute_environment = {
            "id": attribute_id,
            "class_id": class_id,
            "module_id": class_id.rsplit(".", 1)[0],
            "name": match.group("attribute_name"),
            "prefix": prefix,
            "value": match_in_line.group("attribute_value"),
            "line_number": _line_number+line_number,
            "description": get_docstring(_line_number, lines)
        }
        environment[attribute_id] = attribute_environment

    return environment


def get_function_environment(content, module_id):
    """Return function environment from *content*.

    *module_id* represent the ID of the module.

    """
    environment = {}

    lines = content.split("\n")
    content = filter_comments(content)
    content = collapse_all(content)[0]

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

            function_environment = {
                "id": function_id,
                "module_id": module_id,
                "exported": match.group("export") is not None,
                "default": match.group("default") is not None,
                "name": match.group("function_name"),
                "arguments": arguments,
                "line_number": line_number,
                "description": get_docstring(line_number, lines)
            }
            environment[function_id] = function_environment

    return environment


def get_data_environment(content, module_id):
    """Return data environment from *content*.

    *module_id* represent the ID of the module.

    """
    environment = {}

    lines = content.split("\n")
    content = filter_comments(content)
    content = collapse_all(content)[0]

    for match in DATA_PATTERN.finditer(content):
        data_id = ".".join([module_id, match.group("data_name")])
        line_number = content[:match.start()].count("\n")+1

        # As we collapsed all contexts to avoid noises, we need to get the
        # value from the original data in case it represents an object.
        match_in_line = DATA_PATTERN.search(
            "\n".join(lines[line_number-1:])
        )

        data_environment = {
            "id": data_id,
            "module_id": module_id,
            "exported": match.group("export") is not None,
            "default": match.group("default") is not None,
            "name": match.group("data_name"),
            "value": match_in_line.group("data_value"),
            "type": match.group("data_type"),
            "line_number": line_number,
            "description": get_docstring(line_number, lines)
        }
        environment[data_id] = data_environment

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
        if len(line) == 0 or line.startswith("//"):
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


def filter_comments(content, keep_content_size=False):
    """Return *content* without the comments.

    If *keep_content_size* is set to True, the size of the content is preserved.

    .. note::

        The line numbers are preserved.

    """
    def _replace_comment(element):
        count = element.group().count("\n")
        if keep_content_size:
            _buffer = len(element.group()) - count
            return " " * _buffer + "\n" * count
        return "\n" * count

    content = ONE_LINE_COMMENT_PATTERN.sub(_replace_comment, content)
    content = MULTI_LINES_COMMENT_PATTERN.sub(_replace_comment, content)

    return content


def collapse_all(content, filter_comment=False):
    """Return tuple of *content* with the top level elements only and dictionary
    containing the collapsed content associated with the line number**.

    If *filter_comment* is set to True, all comment are removed from the content
    before collapsing the elements. The collapsed content dictionary preserve
    the comments.

    .. note::

        The line numbers are preserved of the content.

    """
    _initial_content = content
    collapsed_content = {}

    if filter_comment:
        # Filter comment before collapsing elements to prevent comment analysis
        content = filter_comments(content, keep_content_size=True)

    def _replace_comment(element):
        # Guess line number
        count = element.group().count("\n")

        # Ensure that the replacement string keep the same length that
        # the original content to be able to use the match positions
        _buffer = len(element.group()) - count - 2

        if len(element.group()) > 2:
            line_number = content[:element.start()].count("\n")+1
            collapsed_content[line_number] = (
                _initial_content[element.start():element.end()]
            )

        return "<>{buffer}{lines}".format(
            buffer=" " * _buffer,
            lines="\n" * count
        )

    _content = None

    while _content != content:
        _content = content
        content = re.sub(r"{[^{}]*}", _replace_comment, content)

    # Remove the space buffer before returning the content
    content = re.sub(r"<> *", lambda x: "{}", content)

    return content, collapsed_content


def guess_module_name(name, hierarchy_folders, module_names):
    """Return the full module *name* from *hierarchy_folders*.

    *module_names* is the list of modules already recorded.

    """
    for i in range(len(hierarchy_folders)):
        root_module = ".".join(hierarchy_folders[i:])
        if root_module in module_names:
            return ".".join([root_module, name])

    return name
