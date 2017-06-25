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
            " * Base Class\n"
            " */\n"
            "class MotherClass {\n"
            "    constructor() {\n"
            "        this.attribute = 42\n"
            "    }\n"
            "}\n"
            "\n"
            "const CustomWelcome = class Welcome {\n"
            "    greeting() {\n"
            "        return 'Hello World';\n"
            "    }\n"
            "};\n"
            "\n"
            "/**\n"
            " * Inherited class\n"
            " */\n"
            "export default class AwesomeClass extends MotherClass {\n"
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
        )

    return doc_folder


def test_directive_autoclass(doc_folder_with_code):
    """Generate documentation from classes.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.MotherClass\n"
            "\n"
            ".. js:autoclass:: example.CustomWelcome\n"
            "\n"
            ".. js:autoclass:: example.AwesomeClass\n"
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
            "class example.MotherClass()\n"
            "\n"
            "   Base Class\n"
            "\n"
            "class example.CustomWelcome()\n"
            "\n"
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
        )


def test_directive_autoclass_with_members(doc_folder_with_code):
    """Generate documentation from classes with all members.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.MotherClass\n"
            "    :members:\n"
            "\n"
            ".. js:autoclass:: example.CustomWelcome\n"
            "    :members:\n"
            "\n"
            ".. js:autoclass:: example.AwesomeClass\n"
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
            "class example.MotherClass()\n"
            "\n"
            "   Base Class\n"
            "\n"
            "class example.CustomWelcome()\n"
            "\n"
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "   constructor(name)\n"
            "\n"
            "      Constructor.\n"
            "\n"
            "   get name()\n"
            "\n"
            "      Get name.\n"
            "\n"
            "      Warning: The name is awesome\n"
            "\n"
            "   set name(value)\n"
            "\n"
            "      Set name.\n"
            "\n"
            "      Warning: Keep the name awesome\n"
            "\n"
            "   awesomeMethod()\n"
            "\n"
            "      awesomeMethod.\n"
            "\n"
            "   static staticMethod()\n"
            "\n"
            "      staticMethod.\n"
            "\n"
            "   static attribute = 42\n"
            "\n"
            "      attribute.\n"
            "\n"
            "   classicAttribute = { test: a test, }\n"
            "\n"
            "      another attribute.\n"
        )


def test_directive_autoclass_with_specific_members(doc_folder_with_code):
    """Generate documentation from classes with specific members.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.AwesomeClass\n"
            "    :members: name, awesomeMethod\n"
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
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "   get name()\n"
            "\n"
            "      Get name.\n"
            "\n"
            "      Warning: The name is awesome\n"
            "\n"
            "   set name(value)\n"
            "\n"
            "      Set name.\n"
            "\n"
            "      Warning: Keep the name awesome\n"
            "\n"
            "   awesomeMethod()\n"
            "\n"
            "      awesomeMethod.\n"
        )


def test_directive_autoclass_with_default_members(doc_folder_with_code):
    """Generate documentation from classes with all members by default.
    """
    conf_file = os.path.join(doc_folder_with_code, "conf.py")
    with open(conf_file, "a") as f:
        f.write("\njs_class_options = ['members']")

    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.MotherClass\n"
            "\n"
            ".. js:autoclass:: example.CustomWelcome\n"
            "\n"
            ".. js:autoclass:: example.AwesomeClass\n"
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
            "class example.MotherClass()\n"
            "\n"
            "   Base Class\n"
            "\n"
            "class example.CustomWelcome()\n"
            "\n"
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "   constructor(name)\n"
            "\n"
            "      Constructor.\n"
            "\n"
            "   get name()\n"
            "\n"
            "      Get name.\n"
            "\n"
            "      Warning: The name is awesome\n"
            "\n"
            "   set name(value)\n"
            "\n"
            "      Set name.\n"
            "\n"
            "      Warning: Keep the name awesome\n"
            "\n"
            "   awesomeMethod()\n"
            "\n"
            "      awesomeMethod.\n"
            "\n"
            "   static staticMethod()\n"
            "\n"
            "      staticMethod.\n"
            "\n"
            "   static attribute = 42\n"
            "\n"
            "      attribute.\n"
            "\n"
            "   classicAttribute = { test: a test, }\n"
            "\n"
            "      another attribute.\n"
        )


def test_directive_autoclass_without_constructor(doc_folder_with_code):
    """Generate documentation from classes without constructors.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.AwesomeClass\n"
            "    :members:\n"
            "    :skip-constructor:\n"
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
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "   get name()\n"
            "\n"
            "      Get name.\n"
            "\n"
            "      Warning: The name is awesome\n"
            "\n"
            "   set name(value)\n"
            "\n"
            "      Set name.\n"
            "\n"
            "      Warning: Keep the name awesome\n"
            "\n"
            "   awesomeMethod()\n"
            "\n"
            "      awesomeMethod.\n"
            "\n"
            "   static staticMethod()\n"
            "\n"
            "      staticMethod.\n"
            "\n"
            "   static attribute = 42\n"
            "\n"
            "      attribute.\n"
            "\n"
            "   classicAttribute = { test: a test, }\n"
            "\n"
            "      another attribute.\n"
        )


def test_directive_autoclass_without_constructor_default(doc_folder_with_code):
    """Generate documentation from classes without constructors by default.
    """
    conf_file = os.path.join(doc_folder_with_code, "conf.py")
    with open(conf_file, "a") as f:
        f.write("\njs_class_options = ['skip-constructor']")

    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.AwesomeClass\n"
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
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "   get name()\n"
            "\n"
            "      Get name.\n"
            "\n"
            "      Warning: The name is awesome\n"
            "\n"
            "   set name(value)\n"
            "\n"
            "      Set name.\n"
            "\n"
            "      Warning: Keep the name awesome\n"
            "\n"
            "   awesomeMethod()\n"
            "\n"
            "      awesomeMethod.\n"
            "\n"
            "   static staticMethod()\n"
            "\n"
            "      staticMethod.\n"
            "\n"
            "   static attribute = 42\n"
            "\n"
            "      attribute.\n"
            "\n"
            "   classicAttribute = { test: a test, }\n"
            "\n"
            "      another attribute.\n"
        )


def test_directive_autoclass_with_undocumented_members(doc_folder_with_code):
    """Generate documentation from classes with undocumented members.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.MotherClass\n"
            "    :members:\n"
            "    :undoc-members:\n"
            "\n"
            ".. js:autoclass:: example.CustomWelcome\n"
            "    :members:\n"
            "    :undoc-members:\n"
            "\n"
            ".. js:autoclass:: example.AwesomeClass\n"
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
            "class example.MotherClass()\n"
            "\n"
            "   Base Class\n"
            "\n"
            "   constructor()\n"
            "\n"
            "class example.CustomWelcome()\n"
            "\n"
            "   greeting()\n"
            "\n"
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "   constructor(name)\n"
            "\n"
            "      Constructor.\n"
            "\n"
            "   get name()\n"
            "\n"
            "      Get name.\n"
            "\n"
            "      Warning: The name is awesome\n"
            "\n"
            "   set name(value)\n"
            "\n"
            "      Set name.\n"
            "\n"
            "      Warning: Keep the name awesome\n"
            "\n"
            "   awesomeMethod()\n"
            "\n"
            "      awesomeMethod.\n"
            "\n"
            "   undocumentedMethod(arg1, arg2)\n"
            "\n"
            "   static staticMethod()\n"
            "\n"
            "      staticMethod.\n"
            "\n"
            "   static attribute = 42\n"
            "\n"
            "      attribute.\n"
            "\n"
            "   classicAttribute = { test: a test, }\n"
            "\n"
            "      another attribute.\n"
        )


def test_directive_autoclass_with_undoc_members_default(doc_folder_with_code):
    """Generate documentation from classes with undocumented members
    by default.
    """
    conf_file = os.path.join(doc_folder_with_code, "conf.py")
    with open(conf_file, "a") as f:
        f.write("\njs_class_options = ['undoc-members']")

    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.MotherClass\n"
            "    :members:\n"
            "\n"
            ".. js:autoclass:: example.CustomWelcome\n"
            "    :members:\n"
            "\n"
            ".. js:autoclass:: example.AwesomeClass\n"
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
            "class example.MotherClass()\n"
            "\n"
            "   Base Class\n"
            "\n"
            "   constructor()\n"
            "\n"
            "class example.CustomWelcome()\n"
            "\n"
            "   greeting()\n"
            "\n"
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "   constructor(name)\n"
            "\n"
            "      Constructor.\n"
            "\n"
            "   get name()\n"
            "\n"
            "      Get name.\n"
            "\n"
            "      Warning: The name is awesome\n"
            "\n"
            "   set name(value)\n"
            "\n"
            "      Set name.\n"
            "\n"
            "      Warning: Keep the name awesome\n"
            "\n"
            "   awesomeMethod()\n"
            "\n"
            "      awesomeMethod.\n"
            "\n"
            "   undocumentedMethod(arg1, arg2)\n"
            "\n"
            "   static staticMethod()\n"
            "\n"
            "      staticMethod.\n"
            "\n"
            "   static attribute = 42\n"
            "\n"
            "      attribute.\n"
            "\n"
            "   classicAttribute = { test: a test, }\n"
            "\n"
            "      another attribute.\n"
        )


def test_directive_autoclass_with_private_members(doc_folder_with_code):
    """Generate documentation from classes with private members.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.AwesomeClass\n"
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
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "   constructor(name)\n"
            "\n"
            "      Constructor.\n"
            "\n"
            "   get name()\n"
            "\n"
            "      Get name.\n"
            "\n"
            "      Warning: The name is awesome\n"
            "\n"
            "   set name(value)\n"
            "\n"
            "      Set name.\n"
            "\n"
            "      Warning: Keep the name awesome\n"
            "\n"
            "   awesomeMethod()\n"
            "\n"
            "      awesomeMethod.\n"
            "\n"
            "   _privateMethod(arg1)\n"
            "\n"
            "      Private Method.\n"
            "\n"
            "   static staticMethod()\n"
            "\n"
            "      staticMethod.\n"
            "\n"
            "   static attribute = 42\n"
            "\n"
            "      attribute.\n"
            "\n"
            "   classicAttribute = { test: a test, }\n"
            "\n"
            "      another attribute.\n"
        )


def test_directive_autoclass_with_private_members_default(doc_folder_with_code):
    """Generate documentation from classes with private members by default.
    """
    conf_file = os.path.join(doc_folder_with_code, "conf.py")
    with open(conf_file, "a") as f:
        f.write("\njs_class_options = ['private-members']")

    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.AwesomeClass\n"
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
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
            "\n"
            "   constructor(name)\n"
            "\n"
            "      Constructor.\n"
            "\n"
            "   get name()\n"
            "\n"
            "      Get name.\n"
            "\n"
            "      Warning: The name is awesome\n"
            "\n"
            "   set name(value)\n"
            "\n"
            "      Set name.\n"
            "\n"
            "      Warning: Keep the name awesome\n"
            "\n"
            "   awesomeMethod()\n"
            "\n"
            "      awesomeMethod.\n"
            "\n"
            "   _privateMethod(arg1)\n"
            "\n"
            "      Private Method.\n"
            "\n"
            "   static staticMethod()\n"
            "\n"
            "      staticMethod.\n"
            "\n"
            "   static attribute = 42\n"
            "\n"
            "      attribute.\n"
            "\n"
            "   classicAttribute = { test: a test, }\n"
            "\n"
            "      another attribute.\n"
        )


def test_directive_autoclass_with_alias(doc_folder_with_code):
    """Generate documentation from classes with alias.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.MotherClass\n"
            "    :alias: AliasedMotherClass\n"
            "\n"
            ".. js:autoclass:: example.CustomWelcome\n"
            "    :alias: AliasedCustomWelcome\n"
            "\n"
            ".. js:autoclass:: example.AwesomeClass\n"
            "    :alias: AliasedAwesomeClass\n"
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
            "class example.AliasedMotherClass()\n"
            "\n"
            "   Base Class\n"
            "\n"
            "class example.AliasedCustomWelcome()\n"
            "\n"
            "class example.AliasedAwesomeClass(name)\n"
            "\n"
            "   \"import AliasedAwesomeClass from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
        )


def test_directive_autoclass_with_module_alias(doc_folder_with_code):
    """Generate documentation from classes with module alias.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.MotherClass\n"
            "    :module-alias: alias_module\n"
            "\n"
            ".. js:autoclass:: example.CustomWelcome\n"
            "    :module-alias: alias_module\n"
            "\n"
            ".. js:autoclass:: example.AwesomeClass\n"
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
            "class alias_module.MotherClass()\n"
            "\n"
            "   Base Class\n"
            "\n"
            "class alias_module.CustomWelcome()\n"
            "\n"
            "class alias_module.AwesomeClass(name)\n"
            "\n"
            "   \"import AwesomeClass from \"alias_module\"\"\n"
            "\n"
            "   Inherited class\n"
        )


def test_directive_autoclass_with_partial_import_forced(doc_folder_with_code):
    """Generate documentation from classes with partial import forced.
    """
    index_file = os.path.join(doc_folder_with_code, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.AwesomeClass\n"
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
            "class example.AwesomeClass(name)\n"
            "\n"
            "   \"import {AwesomeClass} from \"example\"\"\n"
            "\n"
            "   Inherited class\n"
        )
