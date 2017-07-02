# :coding: utf-8

import re
import functools

from .helper import collapse_all
from .helper import get_docstring


#: Regular Expression pattern for data
_DATA_PATTERN = re.compile(
    r"(?P<start_regex>(\n|^)) *(?P<export>export +)?(?P<default>default +)?"
    r"(?P<type>(const|let|var)) (?P<name>[\w._-]+) *= *(?P<value>.+?;)",
    re.DOTALL
)


def fetch_environment(content, module_id):
    """Return data environment dictionary from *content*.

    *module_id* represent the identifier of the module.

    The environment is in the form of::

        {
            "moduleName.DATA": {
                "id": "moduleName.DATA",
                "module_id": "moduleName",
                "exported": False,
                "default": False,
                "name": "DATA",
                "value": "42",
                "type": "const",
                "line_number": 2,
                "description": "Variable doc.\\n\\nDetailed description."
            }
        }

    """
    environment = {}

    lines = content.split("\n")

    # The comment filter is made during the collapse content process to
    # preserve the entire value (with semi-colons and docstrings!)
    content, collapsed_content = collapse_all(content, filter_comment=True)

    for match in _DATA_PATTERN.finditer(content):
        data_id = ".".join([module_id, match.group("name")])

        line_number = (
            content[:match.start()].count("\n") +
            match.group("start_regex").count("\n") + 1
        )

        value = match.group("value")
        if "{}" in value and line_number in collapsed_content.keys():
            value = value.replace("{}", collapsed_content[line_number])

        # Do not keep semi-colon in value
        if value.endswith(";"):
            value = value[:-1]

        data_environment = {
            "id": data_id,
            "module_id": module_id,
            "exported": match.group("export") is not None,
            "default": match.group("default") is not None,
            "name": match.group("name"),
            "value": functools.reduce(_clean_value, value.split('\n')).strip(),
            "type": match.group("type"),
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
