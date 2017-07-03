# :coding: utf-8

import pytest
import os
import sys

from sphinx.cmdline import main as sphinx_main
from sphinx.util.osutil import cd


@pytest.fixture()
def doc_folder_with_code(doc_folder):
    """Return Doc folder with Javascript example source code.
    """
    js_source = os.path.join(doc_folder, "example")

    with open(os.path.join(js_source, "index.js"), "w") as f:
        f.write(
            "/**\n"
            " * A cool application.\n"
            " */\n"
            "\n"
            "import {\n"
            "    VARIABLE_OBJECT as ALIASED_VARIABLE_OBJECT\n"
            "} from './test_attribute';\n"
            "\n"
            "\n"
            "const undocumentedFunction = (arg) => {\n"
            "    console.log(arg)\n"
            "};\n"
            "\n"
            "\n"
            "/** A private function */\n"
            "function _privateFunction(arg) {\n"
            "    console.log(arg)\n"
            "}\n"
            "\n"
            "export ALIASED_VARIABLE_OBJECT;\n"
            "export * from './test_class';\n"
        )

    with open(os.path.join(js_source, "test_attribute.js"), "w") as f:
        f.write(
            "/**\n"
            " * A variable\n"
            " *\n"
            " * .. note::\n"
            " *\n"
            " *     A note.\n"
            " */\n"
            "export const VARIABLE_OBJECT = {\n"
            "    key1: 'value1',\n"
            "    key2: 'value2',\n"
            "    key3: 'value3',\n"
            "};\n"
            "\n"
            "/** Another variable. */\n"
            "let VARIABLE_INT = 42;\n"
        )

    with open(os.path.join(js_source, "test_class.js"), "w") as f:
        f.write(
            "/** A file with a great class. */\n"
            "\n"
            "\n"
            "import {Element as AliasedElement} from 'wherever';\n"
            "\n"
            "/**\n"
            " * Inherited class\n"
            " */\n"
            "class AwesomeClass {\n"
            "\n"
            "    /**\n"
            "     * Constructor.\n"
            "     */\n"
            "    constructor(name) {\n"
            "        super();\n"
            "        this.name = name;\n"
            "    }\n"
            "\n"
            "    /**\n"
            "     * Get name.\n"
            "     *\n"
            "     * .. warning::\n"
            "     *\n"
            "     *     The name is awesome\n"
            "     */\n"
            "    get name() {\n"
            "        return this.name;\n"
            "    }\n"
            "\n"
            "    /**\n"
            "     * Set name.\n"
            "     *\n"
            "     * .. warning::\n"
            "     *\n"
            "     *     Keep the name awesome\n"
            "     */\n"
            "    set name(value) {\n"
            "        this.name = value;\n"
            "    }\n"
            "\n"
            "    /**\n"
            "     * awesomeMethod.\n"
            "     */\n"
            "    awesomeMethod = () => {\n"
            "        console.log('Method has been called');\n"
            "    };\n"
            "\n"
            "    undocumentedMethod(arg1, arg2) {\n"
            "        console.log('An un-documented method has been called');\n"
            "    }\n"
            "\n"
            "    /**\n"
            "     * Private Method.\n"
            "     */\n"
            "    _privateMethod(arg1) {\n"
            "        console.log('An private method has been called');\n"
            "    }\n"
            "\n"
            "    /**\n"
            "     * staticMethod.\n"
            "     */\n"
            "    static staticMethod() {\n"
            "        console.log('Static method has been called');\n"
            "    }\n"
            "\n"
            "    /**\n"
            "     * attribute.\n"
            "     */\n"
            "    static attribute = 42;\n"
            "\n"
            "    /**\n"
            "     * another attribute.\n"
            "     */\n"
            "    classicAttribute = {\n"
            "        test: 'a test',\n"
            "    };\n"
            "}\n"
            "\n"
            "export AliasedElement;\n"
            "export default AwesomeClass;\n"
        )

    return doc_folder


def test_directive_automodule_error(doc_folder_with_code):
    """Do not generate doc for non existing module.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:automodule:: example.wrong"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "r"
    ) as f:
        assert f.read() == ""


def test_directive_automodule(doc_folder_with_code):
    """Generate documentation from modules.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:automodule:: example\n"
            "\n"
            ".. js:automodule:: example.test_attribute\n"
            "\n"
            ".. js:automodule:: example.test_class\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "r"
    ) as f:
        if sys.version_info < (3, 0):
            content = f.read().decode("ascii", "ignore")
        else:
            content = f.read().encode("ascii", "ignore").decode("utf8")

        assert content == (
            "A cool application.\n"
            "\n"
            "A file with a great class.\n"
        )


def test_directive_automodule_with_members(doc_folder_with_code):
    """Generate documentation from modules with members.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:automodule:: example\n"
            "    :members:\n"
            "\n"
            ".. js:automodule:: example.test_attribute\n"
            "    :members:\n"
            "\n"
            ".. js:automodule:: example.test_class\n"
            "    :members:\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "r"
    ) as f:
        if sys.version_info < (3, 0):
            content = f.read().decode("ascii", "ignore")
        else:
            content = f.read().encode("ascii", "ignore").decode("utf8")

        assert content == (
            "A cool application.\n"
            "\n"
            "const example.ALIASED_VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {ALIASED_VARIABLE_OBJECT} from \"example\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import {AwesomeClass} from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "const example.test_attribute.VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {VARIABLE_OBJECT} from \"example/test_attribute\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "let example.test_attribute.VARIABLE_INT = 42\n"
            "\n"
            "   Another variable.\n"
            "\n"
            "A file with a great class.\n"
            "\n"
            "class example.test_class.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example/test_class\"\"\n"
            "\n"
            "   Inherited class\n"
        )


def test_directive_automodule_with_specific_members(doc_folder_with_code):
    """Generate documentation from modules with specific members.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:automodule:: example.test_attribute\n"
            "    :members: VARIABLE_OBJECT\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "r"
    ) as f:
        if sys.version_info < (3, 0):
            content = f.read().decode("ascii", "ignore")
        else:
            content = f.read().encode("ascii", "ignore").decode("utf8")

        assert content == (
            "const example.test_attribute.VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {VARIABLE_OBJECT} from \"example/test_attribute\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
        )


def test_directive_automodule_with_undocumented_members(doc_folder_with_code):
    """Generate documentation from modules with undocumented members.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:automodule:: example\n"
            "    :members:\n"
            "    :undoc-members:\n"
            "\n"
            ".. js:automodule:: example.test_attribute\n"
            "    :members:\n"
            "    :undoc-members:\n"
            "\n"
            ".. js:automodule:: example.test_class\n"
            "    :members:\n"
            "    :undoc-members:\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "r"
    ) as f:
        if sys.version_info < (3, 0):
            content = f.read().decode("ascii", "ignore")
        else:
            content = f.read().encode("ascii", "ignore").decode("utf8")

        assert content == (
            "A cool application.\n"
            "\n"
            "example.undocumentedFunction(arg)\n"
            "\n"
            "const example.ALIASED_VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {ALIASED_VARIABLE_OBJECT} from \"example\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import {AwesomeClass} from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "const example.test_attribute.VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {VARIABLE_OBJECT} from \"example/test_attribute\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "let example.test_attribute.VARIABLE_INT = 42\n"
            "\n"
            "   Another variable.\n"
            "\n"
            "A file with a great class.\n"
            "\n"
            "class example.test_class.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example/test_class\"\"\n"
            "\n"
            "   Inherited class\n"
        )


def test_directive_automodule_with_undocumented_members_default(
    doc_folder_with_code
):
    """Generate documentation from modules with undocumented members by default.
    """
    conf_file = os.path.join(doc_folder_with_code, "conf.py")
    with open(conf_file, "a") as f:
        f.write("\njs_module_options = ['undoc-members']")

    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:automodule:: example\n"
            "    :members:\n"
            "\n"
            ".. js:automodule:: example.test_attribute\n"
            "    :members:\n"
            "\n"
            ".. js:automodule:: example.test_class\n"
            "    :members:\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "r"
    ) as f:
        if sys.version_info < (3, 0):
            content = f.read().decode("ascii", "ignore")
        else:
            content = f.read().encode("ascii", "ignore").decode("utf8")

        assert content == (
            "A cool application.\n"
            "\n"
            "example.undocumentedFunction(arg)\n"
            "\n"
            "const example.ALIASED_VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {ALIASED_VARIABLE_OBJECT} from \"example\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import {AwesomeClass} from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "const example.test_attribute.VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {VARIABLE_OBJECT} from \"example/test_attribute\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "let example.test_attribute.VARIABLE_INT = 42\n"
            "\n"
            "   Another variable.\n"
            "\n"
            "A file with a great class.\n"
            "\n"
            "class example.test_class.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example/test_class\"\"\n"
            "\n"
            "   Inherited class\n"
        )


def test_directive_automodule_with_private_members(doc_folder_with_code):
    """Generate documentation from modules with private members.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:automodule:: example\n"
            "    :members:\n"
            "    :private-members:\n"
            "\n"
            ".. js:automodule:: example.test_attribute\n"
            "    :members:\n"
            "    :private-members:\n"
            "\n"
            ".. js:automodule:: example.test_class\n"
            "    :members:\n"
            "    :private-members:\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "r"
    ) as f:
        if sys.version_info < (3, 0):
            content = f.read().decode("ascii", "ignore")
        else:
            content = f.read().encode("ascii", "ignore").decode("utf8")

        assert content == (
            "A cool application.\n"
            "\n"
            "example._privateFunction(arg)\n"
            "\n"
            "   A private function\n"
            "\n"
            "const example.ALIASED_VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {ALIASED_VARIABLE_OBJECT} from \"example\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import {AwesomeClass} from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "const example.test_attribute.VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {VARIABLE_OBJECT} from \"example/test_attribute\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "let example.test_attribute.VARIABLE_INT = 42\n"
            "\n"
            "   Another variable.\n"
            "\n"
            "A file with a great class.\n"
            "\n"
            "class example.test_class.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example/test_class\"\"\n"
            "\n"
            "   Inherited class\n"
        )


def test_directive_automodule_with_private_members_default(
    doc_folder_with_code
):
    """Generate documentation from modules with private members by default.
    """
    conf_file = os.path.join(doc_folder_with_code, "conf.py")
    with open(conf_file, "a") as f:
        f.write("\njs_module_options = ['private-members']")

    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:automodule:: example\n"
            "    :members:\n"
            "\n"
            ".. js:automodule:: example.test_attribute\n"
            "    :members:\n"
            "\n"
            ".. js:automodule:: example.test_class\n"
            "    :members:\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "r"
    ) as f:
        if sys.version_info < (3, 0):
            content = f.read().decode("ascii", "ignore")
        else:
            content = f.read().encode("ascii", "ignore").decode("utf8")

        assert content == (
            "A cool application.\n"
            "\n"
            "example._privateFunction(arg)\n"
            "\n"
            "   A private function\n"
            "\n"
            "const example.ALIASED_VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {ALIASED_VARIABLE_OBJECT} from \"example\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import {AwesomeClass} from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "const example.test_attribute.VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {VARIABLE_OBJECT} from \"example/test_attribute\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "let example.test_attribute.VARIABLE_INT = 42\n"
            "\n"
            "   Another variable.\n"
            "\n"
            "A file with a great class.\n"
            "\n"
            "class example.test_class.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example/test_class\"\"\n"
            "\n"
            "   Inherited class\n"
        )


def test_directive_automodule_with_module_alias(doc_folder_with_code):
    """Generate documentation from modules with module alias.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:automodule:: example\n"
            "    :members:\n"
            "    :module-alias: alias_module\n"
            "\n"
            ".. js:automodule:: example.test_attribute\n"
            "    :members:\n"
            "    :module-alias: alias_module\n"
            "\n"
            ".. js:automodule:: example.test_class\n"
            "    :members:\n"
            "    :module-alias: alias_module\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "r"
    ) as f:
        if sys.version_info < (3, 0):
            content = f.read().decode("ascii", "ignore")
        else:
            content = f.read().encode("ascii", "ignore").decode("utf8")

        assert content == (
            "A cool application.\n"
            "\n"
            "const alias_module.ALIASED_VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {ALIASED_VARIABLE_OBJECT} from \"example\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "class alias_module.AwesomeClass(name)\n"
            "\n"
            "   \"import {AwesomeClass} from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "const alias_module.VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {VARIABLE_OBJECT} from \"example/test_attribute\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "let alias_module.VARIABLE_INT = 42\n"
            "\n"
            "   Another variable.\n"
            "\n"
            "A file with a great class.\n"
            "\n"
            "class alias_module.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example/test_class\"\"\n"
            "\n"
            "   Inherited class\n"
        )


def test_directive_automodule_with_module_path_alias(doc_folder_with_code):
    """Generate documentation from modules with module path alias.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:automodule:: example\n"
            "    :members:\n"
            "    :module-path-alias: alias/module\n"
            "\n"
            ".. js:automodule:: example.test_attribute\n"
            "    :members:\n"
            "    :module-path-alias: alias/module\n"
            "\n"
            ".. js:automodule:: example.test_class\n"
            "    :members:\n"
            "    :module-path-alias: alias/module\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "r"
    ) as f:
        if sys.version_info < (3, 0):
            content = f.read().decode("ascii", "ignore")
        else:
            content = f.read().encode("ascii", "ignore").decode("utf8")

        assert content == (
            "A cool application.\n"
            "\n"
            "const example.ALIASED_VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {ALIASED_VARIABLE_OBJECT} from \"alias/module\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import {AwesomeClass} from \"alias/module\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "const example.test_attribute.VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {VARIABLE_OBJECT} from \"alias/module\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "let example.test_attribute.VARIABLE_INT = 42\n"
            "\n"
            "   Another variable.\n"
            "\n"
            "A file with a great class.\n"
            "\n"
            "class example.test_class.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"alias/module\"\"\n"
            "\n"
            "   Inherited class\n"
        )


def test_directive_automodule_with_partial_import_forced(doc_folder_with_code):
    """Generate documentation from modules with partial import forced.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:automodule:: example\n"
            "    :members:\n"
            "    :force-partial-import:\n"
            "\n"
            ".. js:automodule:: example.test_attribute\n"
            "    :members:\n"
            "    :force-partial-import:\n"
            "\n"
            ".. js:automodule:: example.test_class\n"
            "    :members:\n"
            "    :force-partial-import:\n"
        )

    with cd(doc_folder_with_code):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(
        os.path.join(doc_folder_with_code, "_build", "index.txt"), "r"
    ) as f:
        if sys.version_info < (3, 0):
            content = f.read().decode("ascii", "ignore")
        else:
            content = f.read().encode("ascii", "ignore").decode("utf8")

        assert content == (
            "A cool application.\n"
            "\n"
            "const example.ALIASED_VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {ALIASED_VARIABLE_OBJECT} from \"example\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import {AwesomeClass} from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "const example.test_attribute.VARIABLE_OBJECT = "
            "{ key1: value1, key2: value2, key3: value3, }\n"
            "\n"
            "   \"import {VARIABLE_OBJECT} from \"example/test_attribute\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "let example.test_attribute.VARIABLE_INT = 42\n"
            "\n"
            "   Another variable.\n"
            "\n"
            "A file with a great class.\n"
            "\n"
            "class example.test_class.AwesomeClass(name)\n"
            "\n"
            "   \"import {AwesomeClass} from \"example/test_class\"\"\n"
            "\n"
            "   Inherited class\n"
        )