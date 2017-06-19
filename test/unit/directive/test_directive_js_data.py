# :coding: utf-8

import pytest
import os
import sys

from sphinx.cmdline import main as sphinx_main
from sphinx.util.osutil import cd


@pytest.fixture()
def content():
    return (
        "/**\n"
        " * A variable\n"
        " *\n"
        " * .. note::\n"
        " *\n"
        " *     A note.\n"
        " */\n"
        "export default const VARIABLE_INT = 42;\n"
        "\n"
        "/**\n"
        " * Another variable\n"
        " *\n"
        " * A citation::\n"
        " *\n"
        " *     A citation\n"
        " */\n"
        "var VARIABLE_OBJECT = {\n"
        "    key1: 'value1',\n"
        "    key2: 'value2',\n"
        "    key3: 'value3',\n"
        "};\n"
        "\n"
        "export let VARIABLE_STRING = 'rosebud';\n"
    )


def test_directive_autodata(doc_folder, content):
    """Generate documentation from global data variables.
    """
    js_source = os.path.join(doc_folder, "example")
    with open(os.path.join(js_source, "index.js"), "w") as f:
        f.write(content)

    index_file = os.path.join(doc_folder, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autodata:: example.VARIABLE_INT\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_OBJECT\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_STRING\n"
        )

    with cd(doc_folder):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(os.path.join(doc_folder, "_build", "index.txt"), "r") as f:
        if sys.version_info < (3, 0):
            content = f.read().decode("ascii", "ignore")
        else:
            content = f.read().encode("ascii", "ignore").decode("utf8")

        assert content == (
            "const example.VARIABLE_INT = 42\n"
            "\n"
            "   \"import VARIABLE_INT from \"example\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "var example.VARIABLE_OBJECT = { "
            "key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   Another variable\n"
            "\n"
            "   A citation:\n"
            "\n"
            "      A citation\n"
            "\n"
            "let example.VARIABLE_STRING = rosebud\n"
            "\n"
            "   \"import {VARIABLE_STRING} from \"example\"\"\n"
        )
