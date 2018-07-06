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
        r"[^\w*._\-\\/:% \"()\[\]{}\n=,]", "", value
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
            "\n"
            "export default function() {}\n"
            "\n"
            "/** generator function */\n"
            "const yieldSomethingAliased = function* yieldSomething(arg) {}\n"
        )

    return doc_folder


def test_directive_autofunction(doc_folder_with_code):
    """Generate documentation from functions.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autofunction:: example.doSomething1\n"
            "\n"
            ".. js:autofunction:: example.doSomething2\n"
            "\n"
            ".. js:autofunction:: example.doSomething3\n"
            "\n"
            ".. js:autofunction:: example.__ANONYMOUS_FUNCTION__\n"
            "\n"
            ".. js:autofunction:: example.yieldSomethingAliased\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["-c", ".", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "rb"
    ) as f:
        content = _sanitise_value(f.read())

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
            "\n"
            "example.__ANONYMOUS_FUNCTION__()\n"
            "\n"
            "function* example.yieldSomethingAliased(arg)\n"
            "\n"
            "   generator function\n"
        )


def test_directive_autofunction_with_alias(doc_folder_with_code):
    """Generate documentation from functions with alias.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autofunction:: example.doSomething1\n"
            "    :alias: aliased_doSomething1\n"
            "\n"
            ".. js:autofunction:: example.doSomething2\n"
            "    :alias: aliased_doSomething2\n"
            "\n"
            ".. js:autofunction:: example.doSomething3\n"
            "    :alias: aliased_doSomething3\n"
            "\n"
            ".. js:autofunction:: example.__ANONYMOUS_FUNCTION__\n"
            "    :alias: alias_anonymous\n"
            "\n"
            ".. js:autofunction:: example.yieldSomethingAliased\n"
            "    :alias: aliased_generate\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["-c", ".", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "rb"
    ) as f:
        content = _sanitise_value(f.read())

        assert content == (
            "example.aliased_doSomething1(arg1, arg2 = null)\n"
            "\n"
            "   \"import aliased_doSomething1 from \"example\"\"\n"
            "\n"
            "   A function\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "example.aliased_doSomething2(arg)\n"
            "\n"
            "   Another function\n"
            "\n"
            "   A citation:\n"
            "\n"
            "      A citation\n"
            "\n"
            "example.aliased_doSomething3()\n"
            "\n"
            "   \"import {aliased_doSomething3} from \"example\"\"\n"
            "\n"
            "example.alias_anonymous()\n"
            "\n"
            "function* example.aliased_generate(arg)\n"
            "\n"
            "   generator function\n"
        )


def test_directive_autofunction_with_module_alias(doc_folder_with_code):
    """Generate documentation from functions with module alias.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autofunction:: example.doSomething1\n"
            "    :module-alias: alias_module\n"
            "\n"
            ".. js:autofunction:: example.doSomething2\n"
            "    :module-alias: alias_module\n"
            "\n"
            ".. js:autofunction:: example.doSomething3\n"
            "    :module-alias: alias_module\n"
            "\n"
            ".. js:autofunction:: example.__ANONYMOUS_FUNCTION__\n"
            "    :module-alias: alias_module\n"
            "\n"
            ".. js:autofunction:: example.yieldSomethingAliased\n"
            "    :module-alias: alias_module\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["-c", ".", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "rb"
    ) as f:
        content = _sanitise_value(f.read())

        assert content == (
            "alias_module.doSomething1(arg1, arg2 = null)\n"
            "\n"
            "   \"import doSomething1 from \"example\"\"\n"
            "\n"
            "   A function\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "alias_module.doSomething2(arg)\n"
            "\n"
            "   Another function\n"
            "\n"
            "   A citation:\n"
            "\n"
            "      A citation\n"
            "\n"
            "alias_module.doSomething3()\n"
            "\n"
            "   \"import {doSomething3} from \"example\"\"\n"
            "\n"
            "alias_module.__ANONYMOUS_FUNCTION__()\n"
            "\n"
            "function* alias_module.yieldSomethingAliased(arg)\n"
            "\n"
            "   generator function\n"
        )


def test_directive_autofunction_with_module_path_alias(doc_folder_with_code):
    """Generate documentation from functions with module path alias.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autofunction:: example.doSomething1\n"
            "    :module-path-alias: test/alias/module\n"
            "\n"
            ".. js:autofunction:: example.doSomething2\n"
            "    :module-path-alias: test/alias/module\n"
            "\n"
            ".. js:autofunction:: example.doSomething3\n"
            "    :module-path-alias: test/alias/module\n"
            "\n"
            ".. js:autofunction:: example.__ANONYMOUS_FUNCTION__\n"
            "    :module-path-alias: test/alias/module\n"
            "\n"
            ".. js:autofunction:: example.yieldSomethingAliased\n"
            "    :module-path-alias: test/alias/module\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["-c", ".", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "rb"
    ) as f:
        content = _sanitise_value(f.read())

        assert content == (
            "example.doSomething1(arg1, arg2 = null)\n"
            "\n"
            "   \"import doSomething1 from \"test/alias/module\"\"\n"
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
            "   \"import {doSomething3} from \"test/alias/module\"\"\n"
            "\n"
            "example.__ANONYMOUS_FUNCTION__()\n"
            "\n"
            "function* example.yieldSomethingAliased(arg)\n"
            "\n"
            "   generator function\n"
        )


def test_directive_autofunction_with_partial_import_forced(
    doc_folder_with_code
):
    """Generate documentation from functions with partial import forced.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autofunction:: example.doSomething1\n"
            "    :force-partial-import:\n"
            "\n"
            ".. js:autofunction:: example.doSomething2\n"
            "    :force-partial-import:\n"
            "\n"
            ".. js:autofunction:: example.doSomething3\n"
            "    :force-partial-import:\n"
            "\n"
            ".. js:autofunction:: example.__ANONYMOUS_FUNCTION__\n"
            "    :force-partial-import:\n"
            "\n"
            ".. js:autofunction:: example.yieldSomethingAliased\n"
            "    :force-partial-import:\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["-c", ".", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "rb"
    ) as f:
        content = _sanitise_value(f.read())

        assert content == (
            "example.doSomething1(arg1, arg2 = null)\n"
            "\n"
            "   \"import {doSomething1} from \"example\"\"\n"
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
            "\n"
            "example.__ANONYMOUS_FUNCTION__()\n"
            "\n"
            "function* example.yieldSomethingAliased(arg)\n"
            "\n"
            "   generator function\n"
        )
