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
        " * A function\n"
        " *\n"
        " * .. note::\n"
        " *\n"
        " *     A note.\n"
        " */\n"
        "export default function doSomething1(arg1, arg2 = null) {\n"
        "    console.log('test1')\n"
        "}\n"
        "\n"
        "/**\n"
        " * Another function\n"
        " *\n"
        " * A citation::\n"
        " *\n"
        " *     A citation\n"
        " */\n"
        "const doSomething2 = (arg) => {\n"
        "    console.log('test2')\n"
        "};\n"
        "\n"
        "export const doSomething3 = () => {};\n"
    )


def test_directive_autofunction(doc_folder, content):
    """Generate documentation from functions.
    """
    js_source = os.path.join(doc_folder, "example")
    with open(os.path.join(js_source, "index.js"), "w") as f:
        f.write(content)

    index_file = os.path.join(doc_folder, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autofunction:: example.doSomething1\n"
            "\n"
            ".. js:autofunction:: example.doSomething2\n"
            "\n"
            ".. js:autofunction:: example.doSomething3\n"
        )

    with cd(doc_folder):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(os.path.join(doc_folder, "_build", "index.txt"), "r") as f:
        if sys.version_info < (3, 0):
            content = f.read().decode("ascii", "ignore")
        else:
            content = f.read().encode("ascii", "ignore").decode("utf8")

        assert content == (
            "example.doSomething1(arg1, arg2 = null)\n"
            "\n"
            "   \"import doSomething1 from \"example\"\"\n"
            "\n"
            "   A function\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "example.doSomething2(arg)\n"
            "\n"
            "   Another function\n"
            "\n"
            "   A citation:\n"
            "\n"
            "      A citation\n"
            "\n"
            "example.doSomething3()\n"
            "\n"
            "   \"import {doSomething3} from \"example\"\"\n"
        )
