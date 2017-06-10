# :coding: utf-8

import re
import os


#: Regular Expression pattern for single line comments
ONE_LINE_COMMENT_PATTERN = re.compile(r"//.*?\n")

#: Regular Expression pattern for multi-line comments
MULTI_LINES_COMMENT_PATTERN = re.compile(r"/\*(.|\n)*?\*/")

#: Regular Expression pattern for nested element symbols
NESTED_ELEMENT_PATTERN = re.compile(r"{[^{}]+}")

#: Regular Expression pattern for imported element
IMPORTED_ELEMENT_PATTERN = re.compile(
    r"(?P<start_regex>(\n|^)) *import +"
    r"(?P<expression>({([^{}]|\n)+}|.+))"
    r" +from +['\"](?P<module>[\w/.\\_-]+)['\"];?"
)

#: Regular Expression pattern for exported element
EXPORTED_ELEMENT_PATTERN = re.compile(
    r"(?P<start_regex>(\n|^)) *export +(?P<default>default +)?"
    r"((?P<expression_from_module>({([^{}]|\n)+}|.+))"
    r" +from +['\"](?P<module>[\w/.\\_-]+)['\"]|"
    r"(?P<expression_from_variable>({([^{}]|\n)+}|.+)));?"
)

#: Regular Expression pattern for binding element
BINDING_ELEMENT_PATTERN = re.compile(
    r"^(?P<name>(\w+|\*))( +as +(?P<alias>\w+))?$"
)


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

    def _replace_element(element):
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
        content = NESTED_ELEMENT_PATTERN.sub(_replace_element, content)

    # Remove the space buffer before returning the content
    content = re.sub(r"<> *", lambda x: "{}", content)

    return content, collapsed_content


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


def get_import_environment(content, module_id):
    """Return import environment from *content*.

    *module_id* represent the ID of the module.

    """
    environment = {}

    module_path = module_id.replace(".", os.sep)
    wildcards_number = 0

    for match in IMPORTED_ELEMENT_PATTERN.finditer(content):
        from_module_path = os.path.normpath(
            os.path.join(module_path, match.group("module"))
        )
        from_module_id = from_module_path.replace(os.sep, ".")

        element_raw = match.group("expression").replace("\n", "")

        _env, wildcards_number = get_expression_environment(
            element_raw, from_module_id,
            wildcards_number=wildcards_number,
            environment=environment
        )
        environment.update(_env)

    return environment


def get_export_environment(content, module_id):
    """Return export environment from *content*.

    *module_id* represent the ID of the module.

    """
    environment = {}

    module_path = module_id.replace(".", os.sep)
    wildcards_number = 0

    lines = content.split("\n")

    for match in EXPORTED_ELEMENT_PATTERN.finditer(content):
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

        _env, wildcards_number = get_expression_environment(
            element_raw, from_module_id,
            wildcards_number=wildcards_number,
        )

        environment[line_number] = {
            "description": get_docstring(line_number, lines),
            "line_number": line_number,
            "default": match.group("default") is not None,
            "export": _env
        }

    return environment


def get_expression_environment(
    expression, module_id=None, environment=None, wildcards_number=0
):
    """Return tuple of *expression* environment and updated *wildcards_number*.

    *module_id* is the optional module id from which the expression can
    be resolved.

    Update the *environment* if available and return it as-is if the file
    is not readable.

    *wildcards_number* represent the number of `*` found as un-aliased binding.

    """
    if environment is None:
        environment = {}

    # Parse partial expressions first
    for partial_match in re.finditer("{[^{}]+}", expression):
        for _env in get_binding_environment(
            partial_match.group()[1:-1]
        ):
            element_id = _env["id"]
            environment[element_id] = _env
            environment[element_id].update(
                {"partial": True, "module": module_id}
            )

        # remove partial imports from expression
        expression = (
            expression[:partial_match.start()] +
            " " * len(partial_match.group()) +
            expression[partial_match.end():]
        )

    # Then parse the default expressions
    for _env in get_binding_environment(expression):
        element_id = _env["id"]
        if element_id == "*":
            wildcards_number += 1
            element_id = "WILDCARD_{0}".format(wildcards_number)

        environment[element_id] = _env
        environment[element_id].update(
            {"partial": False, "module": module_id}
        )

    return environment, wildcards_number


def get_binding_environment(expression):
    """Return list of binding environments from *expression*.

    Example::

        expression = "Module1 as ModuleAlias, Module2"
        env = get_import_module_environment(expression)

    The result would be::

        {
            "ModuleAlias": {
                "name": "Module1",
                "alias": "ModuleAlias"
            },
            "Module2": {
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

        match = BINDING_ELEMENT_PATTERN.match(_element)
        if match is None:
            continue

        element_id = match.group("alias")
        if element_id is None:
            element_id = match.group("name")

        _module = {
            "id": element_id,
            "name": match.group("name"),
            "alias": match.group("alias")
        }
        environments.append(_module)

    return environments


# export { name1, name2, …, nameN };
# export { variable1 as name1, variable2 as name2, …, nameN };
# export let name1, name2, …, nameN; // also var
# export let name1 = …, name2 = …, …, nameN; // also var, const
#
# export default expression;
# export default function (…) { … } // also class, function*
# export default function name1(…) { … } // also class, function*
# export { name1 as default, … };
#
# export * from …;
# export { name1, name2, …, nameN } from …;
# export { import1 as name1, import2 as name2, …, nameN } from …;
