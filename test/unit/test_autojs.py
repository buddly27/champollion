# :coding: utf-8

from sphinx.cmdline import main as sphinx_main
from sphinx.util.osutil import cd

import os


def test_autojs_autodata(doc_folder):
    """Generate documentation from global data variable.
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
            " *\n"
            " * A citation::\n"
            " *\n"
            " *     A citation\n"
            " */\n"
            "const TEST = 42;\n"
        )

    index_file = os.path.join(doc_folder, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autodata:: example.TEST"
        )

    with cd(doc_folder):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(os.path.join(doc_folder, "_build", "index.txt"), "r") as f:
        assert f.read() == (
            "const example.TEST\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "   A citation:\n"
            "\n"
            "      A citation\n"
        )
