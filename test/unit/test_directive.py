# :coding: utf-8

from sphinx.cmdline import main as sphinx_main
from sphinx.util.osutil import cd

import os


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
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(os.path.join(doc_folder, "_build", "index.txt"), "r") as f:
        assert f.read().decode("ascii", "ignore") == ""


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
        assert f.read().decode("ascii", "ignore") == (
            "const example.VARIABLE_INT = 42\n"
            "\n"
            "   \"import VARIABLE_INT from \"example\"\"\n"
            "\n"
            "   A variable\n"
            "\n"
            "   Note: A note.\n"
            "\n"
            "var example.VARIABLE_OBJECT = {\n"
            "    key1: value1,\n"
            "    key2: value2,\n"
            "    key3: value3,\n"
            "}\n"
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


def test_directive_autofunction(doc_folder):
    """Generate documentation from functions.
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
        )

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
        assert f.read().decode("ascii", "ignore") == (
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


def test_directive_autoclass(doc_folder):
    """Generate documentation from classes.
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
            "     * awesomeMethod1.\n"
            "     */\n"
            "    awesomeMethod1 = () => {\n"
            "        console.log('Method 1 has been called');\n"
            "    };\n"
            "\n"
            "    /**\n"
            "     * awesomeMethod2.\n"
            "     */\n"
            "    awesomeMethod2(arg1, arg2) {\n"
            "        console.log('Method 2 has been called');\n"
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

    index_file = os.path.join(doc_folder, "index.rst")
    with open(index_file, "w") as f:
        f.write(
            ".. js:autoclass:: example.MotherClass\n"
            "\n"
            ".. js:autoclass:: example.CustomWelcome\n"
            "\n"
            ".. js:autoclass:: example.AwesomeClass\n"
        )

    with cd(doc_folder):
        sphinx_main(["dummy", "-b", "text", "-E", ".", "_build"])

    with open(os.path.join(doc_folder, "_build", "index.txt"), "r") as f:
        assert f.read().decode("ascii", "ignore") == (
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
            "class example.AwesomeClass()\n"
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
            "   awesomeMethod1()\n"
            "\n"
            "      awesomeMethod1.\n"
            "\n"
            "   awesomeMethod2(arg1, arg2)\n"
            "\n"
            "      awesomeMethod2.\n"
            "\n"
            "   static staticMethod()\n"
            "\n"
            "      staticMethod.\n"
            "\n"
            "   static attribute = 42\n"
            "\n"
            "      attribute.\n"
            "\n"
            "   classicAttribute = {\n"
            "           test: a test,\n"
            "       }\n"
            "\n"
            "      another attribute.\n"
        )
