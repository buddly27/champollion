# :coding: utf-8

import re

from .helper import filter_comments
from .helper import collapse_all
from .helper import get_docstring


#: Regular Expression pattern for data
DATA_PATTERN = re.compile(
    r"(?P<export>export +)?(?P<default>default +)?"
    r"(?P<data_type>(const|let|var)) (?P<data_name>\w+) "
    r"*= *(?P<data_value>[^;]+);"
)


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
