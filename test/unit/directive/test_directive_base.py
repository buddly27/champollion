# :coding: utf-8

import pytest
import os

from sphinx.cmdline import main as sphinx_main
from sphinx.util.osutil import cd


def test_directive_error(doc_folder):
    """Do not generate doc for non existing data.
    """
    js_source = os.path.join(doc_folder, "example")
    with open(os.path.join(js_source, "index.js"), "w") as f:
        f.write(
            "/**\n"
            " * A variable\n"
            " *\n"
            " * .. note::\n"
            " *\n"
            " *     A note.\n"
            " */\n"
            "const VARIABLE = 42;\n"
        )

    index_file = os.path.join(doc_folder, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autodata:: example.UNEXISTING_VARIABLE"
        )

    with cd(doc_folder):
        sphinx_main(["-c", ".", "-b", "text", "-E", ".", "_build"])

    with open(os.path.join(doc_folder, "_build", "index.txt"), "r") as f:
        assert f.read() == ""
