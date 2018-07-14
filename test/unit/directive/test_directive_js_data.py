# :coding: utf-8

import pytest
import os
import re
import unicodedata

from sphinx.cmdline import main as sphinx_main
from sphinx.util.osutil import cd


def _sanitise_value(value):
    """Return *value* suitable for comparison using python 2 and python 3.
    """
    value = value.decode("UTF-8")
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("UTF-8")
    value = re.sub(
        r"[^\w._\-\\/:% \"()\[\]{}\n=,]", "", value
    )
    return value


@pytest.fixture()
def doc_folder_with_code(doc_folder):
    """Return Doc folder with Javascript example source code.
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

    return doc_folder


def test_directive_autodata(doc_folder_with_code):
    """Generate documentation from global data variables.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autodata:: example.VARIABLE_INT\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_OBJECT\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_STRING\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["-c", ".", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "rb"
    ) as f:
        content = _sanitise_value(f.read())

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


def test_directive_autodata_with_alias(doc_folder_with_code):
    """Generate documentation from global data variables with alias.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autodata:: example.VARIABLE_INT\n"
            "    :alias: ALIASED_VARIABLE_INT\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_OBJECT\n"
            "    :alias: ALIASED_VARIABLE_OBJECT\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_STRING\n"
            "    :alias: ALIASED_VARIABLE_STRING\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["-c", ".", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "rb"
    ) as f:
        content = _sanitise_value(f.read())

        assert content == (
            "const example.ALIASED_VARIABLE_INT = 42\n"
            "\n"
            "   \"import ALIASED_VARIABLE_INT from \"example\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "var example.ALIASED_VARIABLE_OBJECT = { "
            "key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   Another variable\n"
            "\n"
            "   A citation:\n"
            "\n"
            "      A citation\n"
            "\n"
            "let example.ALIASED_VARIABLE_STRING = rosebud\n"
            "\n"
            "   \"import {ALIASED_VARIABLE_STRING} from \"example\"\"\n"
        )


def test_directive_autodata_with_module_alias(doc_folder_with_code):
    """Generate documentation from global data variables with module alias.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autodata:: example.VARIABLE_INT\n"
            "    :module-alias: alias_module\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_OBJECT\n"
            "    :module-alias: alias_module\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_STRING\n"
            "    :module-alias: alias_module\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["-c", ".", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "rb"
    ) as f:
        content = _sanitise_value(f.read())

        assert content == (
            "const alias_module.VARIABLE_INT = 42\n"
            "\n"
            "   \"import VARIABLE_INT from \"example\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "var alias_module.VARIABLE_OBJECT = { "
            "key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   Another variable\n"
            "\n"
            "   A citation:\n"
            "\n"
            "      A citation\n"
            "\n"
            "let alias_module.VARIABLE_STRING = rosebud\n"
            "\n"
            "   \"import {VARIABLE_STRING} from \"example\"\"\n"
        )


def test_directive_autodata_with_module_path_alias(doc_folder_with_code):
    """Generate documentation from global data variables with module path alias.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autodata:: example.VARIABLE_INT\n"
            "    :module-path-alias: test/alias/module\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_OBJECT\n"
            "    :module-path-alias: test/alias/module\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_STRING\n"
            "    :module-path-alias: test/alias/module\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["-c", ".", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "rb"
    ) as f:
        content = _sanitise_value(f.read())

        assert content == (
            "const example.VARIABLE_INT = 42\n"
            "\n"
            "   \"import VARIABLE_INT from \"test/alias/module\"\"\n"
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
            "   \"import {VARIABLE_STRING} from \"test/alias/module\"\"\n"
        )


def test_directive_autodata_with_partial_import_forced(doc_folder_with_code):
    """Generate documentation from global data variables with partial import
    forced.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autodata:: example.VARIABLE_INT\n"
            "    :force-partial-import:\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_OBJECT\n"
            "    :force-partial-import:\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_STRING\n"
            "    :force-partial-import:\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["-c", ".", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "rb"
    ) as f:
        content = _sanitise_value(f.read())

        assert content == (
            "const example.VARIABLE_INT = 42\n"
            "\n"
            "   \"import {VARIABLE_INT} from \"example\"\"\n"
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


def test_directive_autodata_with_value_skipped(doc_folder_with_code):
    """Generate documentation from global data variables with value skipped.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autodata:: example.VARIABLE_INT\n"
            "    :skip-value:\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_OBJECT\n"
            "    :skip-value:\n"
            "\n"
            ".. js:autodata:: example.VARIABLE_STRING\n"
            "    :skip-value:\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["-c", ".", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "rb"
    ) as f:
        content = _sanitise_value(f.read())

        assert content == (
            "const example.VARIABLE_INT\n"
            "\n"
            "   \"import VARIABLE_INT from \"example\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "var example.VARIABLE_OBJECT\n"
            "\n"
            "   Another variable\n"
            "\n"
            "   A citation:\n"
            "\n"
            "      A citation\n"
            "\n"
            "let example.VARIABLE_STRING\n"
            "\n"
            "   \"import {VARIABLE_STRING} from \"example\"\"\n"
        )
