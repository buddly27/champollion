# :coding: utf-8

import re


#: Regular Expression pattern for single line comments
_ONE_LINE_COMMENT_PATTERN = re.compile(r"(\n|^| )//.*?\n")

#: Regular Expression pattern for multi-line comments
_MULTI_LINES_COMMENT_PATTERN = re.compile(r"/\*.*?\*/", re.DOTALL)

#: Regular Expression pattern for nested element symbols
_NESTED_ELEMENT_PATTERN = re.compile(r"{[^{}]*}")


def filter_comments(
    content, filter_multiline_comment=True, keep_content_size=False
):
    """Return *content* without the comments.

    If *filter_multiline_comment* is set to False, only the one line comment
    will be filtered out.

    If *keep_content_size* is set to True, the size of the content is preserved.

    .. note::

        The filtered content keep the same number of lines as the
        original content.

    .. seealso:: https://www.w3schools.com/js/js_comments.asp

    """
    def _replace_comment(element):
        """Replace matched *element* in content."""
        replacement = ""
        matched = element.group()

        # Ensure that only the comment part is being replaced
        if not matched.startswith("/"):
            replacement += matched[0]
            matched = matched[1:]

        count = matched.count("\n")

        # Add empty spaces with the size of the content if the size
        # must be kept.
        if keep_content_size:
            _buffer = len(matched) - count
            replacement += " " * _buffer + "\n" * count

        # Otherwise simply keep the number of lines
        else:
            replacement += "\n" * count

        return replacement

    content = _ONE_LINE_COMMENT_PATTERN.sub(_replace_comment, content)

    if filter_multiline_comment:
        content = _MULTI_LINES_COMMENT_PATTERN.sub(_replace_comment, content)

    return content


def collapse_all(content, filter_comment=False):
    """Return tuple of *content* with the top level elements only and dictionary
    containing the collapsed content associated with the *line number*.

    If *filter_comment* is set to True, all comment are removed from the content
    before collapsing the elements. The collapsed content dictionary preserve
    the comments.

    .. note::

        The content with collapsed elements keep the same number of
        lines as the original content.

    """
    _initial_content = content
    collapsed_content = {}

    if filter_comment:
        # Filter comment before collapsing elements to prevent comment analysis
        content = filter_comments(content, keep_content_size=True)

    def _replace_element(element):
        """Replace matched *element* in content."""
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
        content = _NESTED_ELEMENT_PATTERN.sub(_replace_element, content)

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
            # Do not look for docstring when more than two blank lines precede
            # the element.
            if index < line_number - 1:
                return

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
            indentation = 2 if len(line) > 1 else 1
            docstring.append(line[indentation:].rstrip())

        # Beginning of valid docstrings starts with '/**'
        elif line.startswith("/**"):
            return "\n".join(docstring[::-1])

        # Error in the docstring
        else:
            return
