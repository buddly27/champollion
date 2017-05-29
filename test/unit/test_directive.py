# :coding: utf-8

from sphinx.cmdline import main as sphinx_main
from sphinx.util.osutil import cd

import os


def test_directive_autodata(doc_folder):
    """Generate documentation from global data variables.
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
            "const TEST_INT = 42;\n"
            "\n"
            "/**\n"
            " * Another variable\n"
            " *\n"
            " * A citation::\n"
            " *\n"
            " *     A citation\n"
            " */\n"
            "var TEST_OBJECT = {\n"
            "    key1: 'value1',\n"
            "    key2: 'value2',\n"
            "    key3: 'value3',\n"
            "};\n"
            "\n"
            "let TEST_STRING = 'rosebud';\n"
        )

    index_file = os.path.join(doc_folder, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autodata:: example.TEST_INT\n"
            "\n"
            ".. js:autodata:: example.TEST_OBJECT\n"
            "\n"
            ".. js:autodata:: example.TEST_STRING\n"
        )

    with cd(doc_folder):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(os.path.join(doc_folder, "_build", "index.txt"), "r") as f:
        assert f.read() == (
            "const example.TEST_INT\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "var example.TEST_OBJECT\n"
            "\n"
            "   Another variable\n"
            "\n"
            "   A citation:\n"
            "\n"
            "      A citation\n"
            "\n"
            "let example.TEST_STRING\n"
        )
