# :coding: utf-8

import re

from .helper import filter_comments
from .helper import collapse_all
from .helper import get_docstring


#: Regular Expression pattern for classes
_CLASS_PATTERN = re.compile(
    r"(?P<start_regex>(\n|^)) *(?P<export>export +)?(?P<default>default +)?"
    r"(class +(?P<class_name>\w+)|(const|let|var) +(?P<data_name>\w+) "
    r"*= *class +\w+)"
    r"( +extends +(?P<mother_class>[\w._-]+))? *{"
)

#: Regular Expression pattern for class methods
_CLASS_METHOD_PATTERN = re.compile(
    r"(?P<start_regex>(\n|^)) *(?P<prefix>(static|get|set) +)?"
    r"(?P<method_name>[\w._-]+) *\([\n ]*(?P<arguments>.*?)[\n ]*\) *{"
)

#: Regular Expression pattern for class arrow methods
_CLASS_METHOD_ARROW_PATTERN = re.compile(
    r"(?P<start_regex>(\n|^)) *(?P<prefix>static +)?(?P<method_name>\w+) *= *"
    r"(\([\n ]*(?P<arguments>.*?)[\n ]*\)|(?P<single_argument>[\w._-]+)) *"
    r"=> *{"
)

#: Regular Expression pattern for class attribute
_CLASS_ATTRIBUTE_PATTERN = re.compile(
    r"(?P<start_regex>(\n|^)) *(?P<prefix>static +)?"
    r"(?P<name>[\w._-]+) *= *"
    r"(?P<value>(\((\n|.)*?\) *=> *{.*?}|\[(\n|.)*?\]|{(\n|.)*?}|"
    r"\((\n|.)*?\)|.+))"
)


def fetch_environment(content, module_id):
    """Return class environment dictionary from *content*.

    *module_id* represent the identifier of the module.

    The environment is in the form of::

        {
            "moduleName.AwesomeClass": {
                "id": "module.AwesomeClass",
                "name": "AwesomeClass",
                "parent": "MotherClass",
                "line": 42,
                "description": "Class doc.\\n\\nDetailed description."

                "id": "moduleName.AwesomeClass",
                "module_id": "moduleName",
                "exported": False,
                "default": False,
                "name": "AwesomeClass",
                "parent": None,
                "line_number": 2,
                "description": "Class doc.\\n\\nDetailed description."
                "method": {
                    "moduleName.AwesomeClass.awesomeMethod": {
                        ....
                    }
                },
                "attribute": {
                    "moduleName.AwesomeClass.DATA": {
                        ....
                    }
                }
            },
            ...
        }

    """
    environment = {}

    lines = content.split("\n")

    # The comment filter is made during the collapse content process to
    # preserve the class content with all comments (and docstrings!)
    content, collapsed_content = collapse_all(content, filter_comment=True)

    for match in _CLASS_PATTERN.finditer(content):
        class_name = match.group("class_name")
        if class_name is None:
            class_name = match.group("data_name")

        class_id = ".".join([module_id, class_name])

        line_number = (
            content[:match.start()].count("\n") +
            match.group("start_regex").count("\n") + 1
        )

        method_environment = {}
        attribute_environment = {}

        if line_number in collapsed_content.keys():
            class_content = collapsed_content[line_number][1:-1]

            method_environment = fetch_methods_environment(
                class_content, class_id, line_number=line_number-1
            )
            attribute_environment = fetch_attribute_environment(
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


def fetch_methods_environment(content, class_id, line_number=0):
    """Return function environment dictionary from *content*.

    *class_id* represent the identifier of the method class.

    *line_number* is the first line number of content.

    The environment is in the form of::

        {
            "moduleName.AwesomeClass.awesomeMethod": {
                "id": "moduleName.AwesomeClass.awesomeMethod",
                "class_id": "moduleName.AwesomeClass",
                "module_id": "moduleName",
                "name": "awesomeMethod",
                "prefix": "get",
                "arguments": ["argument1", "argument2"],
                "line_number": 5,
                "description": "Method doc.\\n\\nDetailed description."
            }
        }

    """
    environment = {}

    lines = content.split("\n")
    content = filter_comments(content)
    content = collapse_all(content)[0]

    for match_iter in (
        _CLASS_METHOD_ARROW_PATTERN.finditer(content),
        _CLASS_METHOD_PATTERN.finditer(content)
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

            _line_number = (
                content[:match.start()].count("\n") +
                match.group("start_regex").count("\n") + 1
            )

            arguments_matched = match.group("arguments")
            if arguments_matched is None:
                arguments_matched = match.group("single_argument")

            arguments = list(filter(lambda x: len(x), [
                arg.strip() for arg in arguments_matched.split(",")
            ]))

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


def fetch_attribute_environment(content, class_id, line_number=0):
    """Return attribute environment dictionary from *content*.

    *class_id* represent the identifier of the attribute class.

    *line_number* is the first line number of content.

    The environment is in the form of::

        {
            "moduleName.AwesomeClass.DATA": {
                "id": "moduleName.AwesomeClass.DATA",
                "class_id": "moduleName.AwesomeClass",
                "module_id": "moduleName",
                "name": "DATA",
                "prefix": "static",
                "value": "42",
                "line_number": 8,
                "description": "Attribute doc.\\n\\nDetailed description."
            }
        }

    """
    environment = {}

    lines = content.split("\n")

    # The comment filter is made during the collapse content process to
    # preserve the entire value (with semi-colons and docstrings!)
    content, collapsed_content = collapse_all(content, filter_comment=True)

    for match in _CLASS_ATTRIBUTE_PATTERN.finditer(content):
        attribute_id = ".".join([class_id, match.group("name")])
        prefix = match.group("prefix")
        if prefix is not None:
            prefix = prefix.strip()

        value = match.group("value")

        _line_number = (
            content[:match.start()].count("\n") +
            match.group("start_regex").count("\n") + 1
        )

        if "{}" in value and _line_number in collapsed_content.keys():
            value = value.replace("{}", collapsed_content[_line_number])

        # Do not keep semi-colon in value
        if value.endswith(";"):
            value = value[:-1]

        attribute_environment = {
            "id": attribute_id,
            "class_id": class_id,
            "module_id": class_id.rsplit(".", 1)[0],
            "name": match.group("name"),
            "prefix": prefix,
            "value": value,
            "line_number": _line_number+line_number,
            "description": get_docstring(_line_number, lines)
        }
        environment[attribute_id] = attribute_environment

    return environment
