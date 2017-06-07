# :coding: utf-8

import re
import functools

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

    # The comment filter is made during the collapse content process to
    # preserve the entire value (with semi-colons and docstrings!)
    content, collapsed_content = collapse_all(content, filter_comment=True)

    for match in DATA_PATTERN.finditer(content):
        data_id = ".".join([module_id, match.group("data_name")])
        line_number = content[:match.start()].count("\n")+1

        value = match.group("data_value")
        if "{}" in value and line_number in collapsed_content.keys():
            value = value.replace("{}", collapsed_content[line_number])

        data_environment = {
            "id": data_id,
            "module_id": module_id,
            "exported": match.group("export") is not None,
            "default": match.group("default") is not None,
            "name": match.group("data_name"),
            "value": functools.reduce(_clean_value, value.split('\n')).strip(),
            "type": match.group("data_type"),
            "line_number": line_number,
            "description": get_docstring(line_number, lines)
        }
        environment[data_id] = data_environment

    return environment


def _clean_value(line1, line2):
    """Clean up variable value for display."""
    _line1 = line1.strip()
    _line2 = line2.strip()

    # Let trailing space to make the code easier to read
    if _line1[-1:] in ["{", "}", "(", ")", "[", "]", ";", ","]:
        _line1 += " "

    return _line1 + _line2
