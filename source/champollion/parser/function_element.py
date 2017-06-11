# :coding: utf-8

import re

from .helper import filter_comments
from .helper import collapse_all
from .helper import get_docstring


#: Regular Expression pattern for function expressions
_FUNCTION_PATTERN = re.compile(
    r"(?P<start_regex>(\n|^)) *(?P<export>export +)?(?P<default>default +)?"
    r"((const|var|let) (?P<data_name>[\w_-]+) *= *)?"
    r"function *(?P<generator>\* *)?(?P<function_name>[\w_-]+)? "
    r"*\([\n ]*(?P<arguments>.*?)[\n ]*\) *{",
)

#: Regular Expression pattern for arrow functions
_FUNCTION_ARROW_PATTERN = re.compile(
    r"(?P<start_regex>(\n|^)) *(?P<export>export +)?(?P<default>default +)?"
    r"(const|let|var) (?P<function_name>\w+) *= *"
    r"(\([\n ]*(?P<arguments>.*?)[\n ]*\)|(?P<single_argument>[\w._-]+)) *"
    r"=> *{"
)


def fetch_environment(content, module_id):
    """Return function environment dictionary from *content*.

    *module_id* represent the identifier of the module.

    The environment is in the form of::

        {
            "moduleName.doSomething": {
                "id": "moduleName.doSomething",
                "module_id": "moduleName",
                "exported": False,
                "default": False,
                "name": "doSomething",
                "anonymous": False,
                "generator": False,
                "arguments": ["argument1", "argument2"],
                "line_number": 2,
                "description": "Function doc.\\n\\nDetailed description."
            }
        }

    """
    environment = {}

    lines = content.split("\n")
    content = filter_comments(content)
    content = collapse_all(content)[0]

    for match_iter in (
        _FUNCTION_ARROW_PATTERN.finditer(content),
        _FUNCTION_PATTERN.finditer(content)
    ):
        for match in match_iter:
            name = match.group("function_name")
            if "data_name" in match.groupdict().keys():
                _name = match.group("data_name")
                if _name is not None:
                    name = _name

            generator = False
            if "generator" in match.groupdict().keys():
                generator = match.group("generator") is not None

            if name is None:
                name = "__ANONYMOUS_FUNCTION__"

            function_id = ".".join([module_id, name])

            line_number = (
                content[:match.start()].count("\n") +
                match.group("start_regex").count("\n") + 1
            )

            arguments_matched = match.group("arguments")
            if arguments_matched is None:
                arguments_matched = match.group("single_argument")

            arguments = list(filter(lambda x: len(x), [
                arg.strip() for arg in arguments_matched.split(",")
            ]))

            function_environment = {
                "id": function_id,
                "module_id": module_id,
                "exported": match.group("export") is not None,
                "default": match.group("default") is not None,
                "name": name,
                "anonymous": name == "__ANONYMOUS_FUNCTION__",
                "generator": generator,
                "arguments": arguments,
                "line_number": line_number,
                "description": get_docstring(line_number, lines)
            }
            environment[function_id] = function_environment

    return environment
