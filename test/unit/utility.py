# :coding: utf-8

import re
import unicodedata

import sphinx


#: Identify the sphinx version.
SPHINX_VERSION = tuple([int(v) for v in sphinx.__version__.split(".")])


def sanitize_value(value):
    """Return *value* suitable for comparison using python 2 and python 3.
    """
    value = value.decode("UTF-8")
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("UTF-8")
    value = re.sub(
        r"[^\w*._\-\\/:% \"()\[\]{}\n=,]", "", value
    )

    # The textwrap used prior to Sphinx 2.3.0 had a different way to format
    # notes and warnings.
    # https://github.com/sphinx-doc/sphinx/commit/5a05cabd6acd7de3929b355a67ca76298f3baa27
    if SPHINX_VERSION < (2, 3, 0):
        value = value.replace("Warning: ", "Warning:\n\n        ")
        value = value.replace("Note: ", "Note:\n\n     ")

    return value
