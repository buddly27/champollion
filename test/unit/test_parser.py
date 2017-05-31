# :coding: utf-8

import pytest
import tempfile
import os

import champollion.parser


def test_get_environment_error():
    """Raise an error if the path is incorrect."""
    with pytest.raises(OSError):
        champollion.parser.get_environment("")


def test_get_environment_empty(temporary_directory):
    """Return an empty environment."""
    environment = {
        "module": {},
        "class": {},
        "method": {},
        "attribute": {},
        "function": {},
        "data": {},
        "file": {}
    }
    assert champollion.parser.get_environment(
        temporary_directory
    ) == environment


def test_get_module_environment_from_file():
    """Return module_id and environment from file id."""
    assert champollion.parser.get_module_environment(
        "test/module/example.js", []
    ) == (
        "test.module.example",
        {
            "module": {
                "test.module.example": {
                    "id": "test.module.example",
                    "name": "example",
                    "file_id": "test/module/example.js"
                }
            }
        }
    )


def test_get_module_environment_from_index_file():
    """Return module_id and environment from index file id."""
    assert champollion.parser.get_module_environment(
        "test/module/index.js", []
    ) == (
        "test.module",
        {
            "module": {
                "test.module": {
                    "id": "test.module",
                    "name": "module",
                    "file_id": "test/module/index.js"
                }
            }
        }
    )


def test_get_module_environment_from_file_with_adjacent_index():
    """Return module_id and environment from file id with adjacent index file.
    """
    assert champollion.parser.get_module_environment(
        "test/module/example.js", ["index.js"]
    ) == (
        "test.module.example",
        {
            "module": {
                "test.module.example": {
                    "id": "test.module.example",
                    "name": "module.example",
                    "file_id": "test/module/example.js"
                }
            }
        }
    )


def test_get_module_environment_from_file_with_initial_environment():
    """Return module_id and updated environment from file id and module id."""
    environment = {
        "module": {
            "test": {}
        },
        "class": {
            "test.AwesomeClass": {}
        },
        "function": {
            "test.doSomething": {}
        },
        "data": {
            "test.DATA": {}
        },
        "file": {
            "path/to/other/example.js": {}
        }
    }

    assert champollion.parser.get_module_environment(
        "test/module/index.js", [], environment
    ) == (
        "test.module",
        {
            "module": {
                "test": {},
                "test.module": {
                    "id": "test.module",
                    "name": "test.module",
                    "file_id": "test/module/index.js"
                }
            },
            "file": {
                "path/to/other/example.js": {}
            },
            "class": {
                "test.AwesomeClass": {}
            },
            "function": {
                "test.doSomething": {}
            },
            "data": {
                "test.DATA": {}
            }
        }
    )


def test_get_file_environment_empty(request):
    """Return environment from empty file."""
    file_handle, path = tempfile.mkstemp(suffix=".js")
    os.close(file_handle)

    assert champollion.parser.get_file_environment(
        path, "path/to/example.js", "test.module"
    ) == {
        "file": {
            "path/to/example.js": {
                "id": "path/to/example.js",
                "module_id": "test.module",
                "name": os.path.basename(path),
                "path": path,
                "content": ""
            }
        },
        "class": {},
        "method": {},
        "attribute": {},
        "function": {},
        "data": {}
    }

    def cleanup():
        """Remove temporary file."""
        try:
            os.remove(path)
        except OSError:
            pass

    request.addfinalizer(cleanup)
    return path


def test_get_file_environment_empty_with_initial_environment(request):
    """Update environment from empty file."""
    file_handle, path = tempfile.mkstemp(suffix=".js")
    os.close(file_handle)

    environment = {
        "module": {
            "test.module": {}
        },
        "class": {
            "test.module.AwesomeClass": {}
        },
        "method": {
            "test.module.AwesomeClass.method": {}
        },
        "attribute": {
            "test.module.AwesomeClass.ATTRIBUTE": {}
        },
        "function": {
            "test.module.doSomething": {}
        },
        "data": {
            "test.module.DATA": {}
        },
        "file": {
            "path/to/other/example.js": {}
        }
    }

    assert champollion.parser.get_file_environment(
        path, "path/to/example.js", "test.module", environment
    ) == {
        "file": {
            "path/to/other/example.js": {},
            "path/to/example.js": {
                "id": "path/to/example.js",
                "module_id": "test.module",
                "name": os.path.basename(path),
                "path": path,
                "content": ""
            }
        },
        "module": {
            "test.module": {}
        },
        "class": {
            "test.module.AwesomeClass": {}
        },
        "method": {
            "test.module.AwesomeClass.method": {}
        },
        "attribute": {
            "test.module.AwesomeClass.ATTRIBUTE": {}
        },
        "function": {
            "test.module.doSomething": {}
        },
        "data": {
            "test.module.DATA": {}
        }
    }

    def cleanup():
        """Remove temporary file."""
        try:
            os.remove(path)
        except OSError:
            pass

    request.addfinalizer(cleanup)
    return path


def test_get_class_environment():
    """Return class environment from content."""
    content = (
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
        "    /** AwesomeClass constructor */\n"
        "    constructor(name) {\n"
        "        super();\n"
        "        this.name = name;\n"
        "    }\n"
        "\n"
        "    /**\n"
        "     * Get the name.\n"
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
        "     * Set the name.\n"
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
        "     * A first awesome method.\n"
        "     */\n"
        "    awesomeMethod1 = () => {\n"
        "        console.log('Method 1 has been called');\n"
        "    };\n"
        "\n"
        "    /**\n"
        "     * A second awesome method.\n"
        "     */\n"
        "    awesomeMethod2(arg1, arg2) {\n"
        "        console.log('Method 2 has been called');\n"
        "    }\n"
        "\n"
        "    /**\n"
        "     * A static method.\n"
        "     */\n"
        "    static staticMethod() {\n"
        "        console.log('Static method has been called');\n"
        "    }\n"
        "\n"
        "    /**\n"
        "     * A static attribute.\n"
        "     */\n"
        "    static attribute = 42;\n"
        "}\n"
    )

    assert champollion.parser.get_class_environment(
        content, "test.module"
    ) == {
        "test.module.MotherClass": {
            "id": "test.module.MotherClass",
            "module_id": "test.module",
            "exported": False,
            "default": False,
            "name": "MotherClass",
            "parent": None,
            "line_number": 4,
            "description": "Base Class",
            "method": {
                "test.module.MotherClass.constructor": {
                    "id": "test.module.MotherClass.constructor",
                    "class_id": "test.module.MotherClass",
                    "module_id": "test.module",
                    "name": "constructor",
                    "prefix": None,
                    "arguments": [],
                    "line_number": 5,
                    "description": None
                }
            },
            "attribute": {}
        },
        "test.module.CustomWelcome": {
            "id": "test.module.CustomWelcome",
            "module_id": "test.module",
            "exported": False,
            "default": False,
            "name": "CustomWelcome",
            "parent": None,
            "line_number": 10,
            "description": None,
            "method": {
                "test.module.CustomWelcome.greeting": {
                    "id": "test.module.CustomWelcome.greeting",
                    "class_id": "test.module.CustomWelcome",
                    "module_id": "test.module",
                    "name": "greeting",
                    "prefix": None,
                    "arguments": [],
                    "line_number": 11,
                    "description": None
                }
            },
            "attribute": {}
        },
        "test.module.AwesomeClass": {
            "id": "test.module.AwesomeClass",
            "module_id": "test.module",
            "exported": True,
            "default": True,
            "name": "AwesomeClass",
            "parent": "MotherClass",
            "line_number": 19,
            "description": "Inherited class",
            "method": {
                "test.module.AwesomeClass.constructor": {
                    "id": "test.module.AwesomeClass.constructor",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "constructor",
                    "prefix": None,
                    "arguments": ["name"],
                    "line_number": 21,
                    "description": "AwesomeClass constructor"
                },
                "test.module.AwesomeClass.name.get": {
                    "id": "test.module.AwesomeClass.name.get",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "name",
                    "prefix": "get",
                    "arguments": [],
                    "line_number": 33,
                    "description": (
                        "Get the name.\n"
                        "\n"
                        ".. warning::\n"
                        "\n"
                        "    The name is awesome"
                    )
                },
                "test.module.AwesomeClass.name.set": {
                    "id": "test.module.AwesomeClass.name.set",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "name",
                    "prefix": "set",
                    "arguments": ["value"],
                    "line_number": 44,
                    "description": (
                        "Set the name.\n"
                        "\n"
                        ".. warning::\n"
                        "\n"
                        "    Keep the name awesome"
                    )
                },
                "test.module.AwesomeClass.awesomeMethod1": {
                    "id": "test.module.AwesomeClass.awesomeMethod1",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "awesomeMethod1",
                    "prefix": None,
                    "arguments": [],
                    "line_number": 51,
                    "description": "A first awesome method."
                },
                "test.module.AwesomeClass.awesomeMethod2": {
                    "id": "test.module.AwesomeClass.awesomeMethod2",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "awesomeMethod2",
                    "prefix": None,
                    "arguments": ["arg1", "arg2"],
                    "line_number": 58,
                    "description": "A second awesome method."
                },
                "test.module.AwesomeClass.staticMethod": {
                    "id": "test.module.AwesomeClass.staticMethod",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "staticMethod",
                    "prefix": "static",
                    "arguments": [],
                    "line_number": 65,
                    "description": "A static method."
                }
            },
            "attribute": {
                "test.module.AwesomeClass.attribute": {
                    "id": "test.module.AwesomeClass.attribute",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "attribute",
                    "prefix": "static",
                    "value": "42",
                    "line_number": 72,
                    "description": "A static attribute."
                }
            }
        },
    }


def test_get_function_environment():
    """Return function environment from content."""
    content = (
        "/** test function */\n"
        "export function doSomething() {\n"
        "    console.log('something');\n"
        "}\n"
        "\n"
        "/**\n"
        " * test function with arguments.\n"
        " */\n"
        "const doSomethingElse = (arg1, arg2) => {\n"
        "    console.log('something_else');\n"
        "};\n"
        "\n"
        "export default const doSomethingWithManyArguments = ("
        "  arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9"
        ") => {};\n"
        "\n"
        ""
    )

    assert champollion.parser.get_function_environment(
        content, "test.module"
    ) == {
        "test.module.doSomething": {
            "id": "test.module.doSomething",
            "module_id": "test.module",
            "exported": True,
            "default": False,
            "name": "doSomething",
            "arguments": [],
            "line_number": 2,
            "description": "test function"
        },
        "test.module.doSomethingElse": {
            "id": "test.module.doSomethingElse",
            "module_id": "test.module",
            "exported": False,
            "default": False,
            "name": "doSomethingElse",
            "arguments": ["arg1", "arg2"],
            "line_number": 9,
            "description": "test function with arguments."
        },
        "test.module.doSomethingWithManyArguments": {
            "id": "test.module.doSomethingWithManyArguments",
            "module_id": "test.module",
            "exported": True,
            "default": True,
            "name": "doSomethingWithManyArguments",
            "arguments": [
                "arg1", "arg2", "arg3", "arg4",
                "arg5", "arg6", "arg7", "arg8",
                "arg9"
            ],
            "line_number": 13,
            "description": None
        },
    }


def test_get_data_environment():
    """Return data environment from content."""
    content = (
        "/** test list data */\n"
        "const test_list = [1, 2, 3];\n"
        "\n"
        "/**\n"
        " * test dictionary data.\n"
        " * \n"
        " * Detailed description.\n"
        " */\n"
        "export default var test_object = {\n"
        "   key1: value1,\n"
        "   key2: value2,\n"
        "   key3: value3,\n"
        "};\n"
        "\n"
        "/** test string data */\n"
        "let test_string ='youpi';\n"
        "\n"
        "export const test_int = 42;\n"
    )

    assert champollion.parser.get_data_environment(
        content, "test.module"
    ) == {
        "test.module.test_list": {
            "id": "test.module.test_list",
            "module_id": "test.module",
            "exported": False,
            "default": False,
            "name": "test_list",
            "type": "const",
            "value": "[1, 2, 3]",
            "line_number": 2,
            "description": "test list data"
        },
        "test.module.test_object": {
            "id": "test.module.test_object",
            "module_id": "test.module",
            "exported": True,
            "default": True,
            "name": "test_object",
            "type": "var",
            "value": (
                "{\n"
                "   key1: value1,\n"
                "   key2: value2,\n"
                "   key3: value3,\n"
                "}"
            ),
            "line_number": 9,
            "description": "test dictionary data.\n\nDetailed description."
        },
        "test.module.test_string": {
            "id": "test.module.test_string",
            "module_id": "test.module",
            "exported": False,
            "default": False,
            "name": "test_string",
            "type": "let",
            "value": "'youpi'",
            "line_number": 16,
            "description": "test string data"
        },
        "test.module.test_int": {
            "id": "test.module.test_int",
            "module_id": "test.module",
            "exported": True,
            "default": False,
            "name": "test_int",
            "type": "const",
            "value": "42",
            "line_number": 18,
            "description": None
        },
    }


@pytest.mark.parametrize(
    ("content_lines", "line_number", "expected"),
    [
        (
            [
                "/**",
                " * An function example.",
                " *",
                " * Detailed description.",
                " *",
                " * .. note::",
                " *",
                " *     A note.",
                " */",
                "function sum(a, b) {",
                "    return a+b;",
                "}",
            ],
            10,
            (
                "An function example.\n"
                "\n"
                "Detailed description.\n"
                "\n"
                ".. note::\n"
                "\n"
                "    A note."
            )
        ),
        (
            [
                "/** A cool data. */",
                "const Data = null",
            ],
            2,
            (
                "A cool data."
            )
        ),
        (
            [
                "/*",
                " * Incorrect docstring",
                " */",
                "function doSomething() {",
                "    console.log('something');",
                "}",
            ],
            4,
            None
        ),
        (
            [
                "/*",
                "",
                " Incorrect docstring",
                "",
                "*/",
                "function doSomethingElse() {",
                "    console.log('something_else');",
                "}",
            ],
            6,
            None
        ),
        (
            [
                "// Incorrect docstring",
                "function doSomethingElse() {",
                "    console.log('something_else');",
                "}",
            ],
            2,
            None
        ),
        (
            [
                "",
                "function doSomethingElse() {",
                "    console.log('something_else');",
                "}",
            ],
            2,
            None
        ),
        (
            [
                "/** A cool data. */",
                "const Data = null",
            ],
            1,
            None
        )
    ],
    ids=[
        "valid element line number with multiline docstring",
        "valid element line number with one line docstring",
        "valid element line number with incorrect docstring 1",
        "valid element line number with incorrect docstring 2",
        "valid element line number with incorrect docstring 3",
        "valid element line number with no docstring",
        "invalid line_number",
    ]
)
def test_get_docstrings(content_lines, line_number, expected):
    """Return docstrings from a element's line number."""
    assert champollion.parser.get_docstring(
        line_number, content_lines
    ) == expected


def test_filter_comments():
    """Remove all comments from content"""
    content = (
        "'use strict'; /* a beautiful comment */\n"
        "\n"
        "/*\n"
        "a long comment that can take a lot of places so\n"
        "we put it on several lines.\n"
        "*/\n"
        "\n"
        "// a data docstring\n"
        "const DATA = 1;\n"
        "\n"
        "/**\n"
        " * Function docstring\n"
        " */\n"
        "function sum(a, b) {\n"
        "    // Return the sum of a and b\n"
        "    return a+b;\n"
        "}\n"
    )

    expected = (
        "'use strict'; \n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "const DATA = 1;\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "function sum(a, b) {\n"
        "    \n"
        "    return a+b;\n"
        "}\n"
    )
    assert champollion.parser.filter_comments(content) == expected


@pytest.mark.parametrize(
    ("content", "expected_content", "expected_collapsed_content"),
    [
        (
            "const emptyObject = {};",
            "const emptyObject = {};",
            {}
        ),
        (
            "let test = {a: 1, b: 2, c: 3};",
            "let test = {};",
            {
                1: "{a: 1, b: 2, c: 3}"
            }
        ),
        (
            (
                "const element = {\n"
                "    key1: value1,\n"
                "    key2: value2,\n"
                "    key3: value3,\n"
                "};\n"
                "\n"
                "function sum(a, b) {\n"
                "    return a+b\n"
                "}\n"
                "\n"
            ),
            (
                "const element = {}\n"
                "\n"
                "\n"
                "\n"
                ";\n"
                "\n"
                "function sum(a, b) {}\n"
                "\n"
                "\n"
                "\n"
            ),
            {
                1: (
                    "{\n"
                    "    key1: value1,\n"
                    "    key2: value2,\n"
                    "    key3: value3,\n"
                    "}"
                ),
                7: "{\n"
                   "    return a+b\n"
                   "}"
            }
        ),
        (
            (
                "class AwesomeClass {\n"
                "    constructor() {\n"
                "        this.data = 1;\n"
                "    }\n"
                "\n"
                "    increase() {\n"
                "        this.data += 1;\n"
                "    }\n"
                "}\n"
            ),
            (
                "class AwesomeClass {}\n"
                "\n"
                "\n"
                "\n"
                "\n"
                "\n"
                "\n"
                "\n"
                "\n"
            ),
            {
                1: (
                    "{\n"
                    "    constructor() {\n"
                    "        this.data = 1;\n"
                    "    }\n"
                    "\n"
                    "    increase() {\n"
                    "        this.data += 1;\n"
                    "    }\n"
                    "}"
                ),
                2: (
                    "{\n"
                    "        this.data = 1;\n"
                    "    }"
                ),
                6: (
                    "{\n"
                    "        this.data += 1;\n"
                    "    }"
                )
            }
        )
    ],
    ids=[
        "empty object",
        "simple object",
        "objects and functions on multiple lines",
        "nested class"
    ]
)
def test_collapse_all(content, expected_content, expected_collapsed_content):
    """Collapse all objects, classes and functions."""
    assert champollion.parser.collapse_all(content) == (
        expected_content, expected_collapsed_content
    )


@pytest.mark.parametrize(
    ("name", "hierarchy_folders", "module_names", "expected"),
    [
        (
            "example",
            ["module", "submodule", "test"],
            [],
            "example"
        ),
        (
            "example",
            ["module", "submodule", "test"],
            ["another_module"],
            "example"
        ),
        (
            "example",
            ["module", "submodule", "test"],
            ["module.submodule.test"],
            "module.submodule.test.example"
        ),
        (
            "example",
            ["module", "submodule", "test"],
            ["submodule.test"],
            "submodule.test.example"
        ),
        (
            "example",
            ["module", "submodule", "test"],
            ["another_module", "submodule.test", "test"],
            "submodule.test.example"
        )
    ],
    ids=[
        "no module",
        "one module not in hierarchy",
        "one module matching entire hierarchy",
        "one module matching part of the hierarchy",
        "several modules"
    ]
)
def test_guess_module_name(name, hierarchy_folders, module_names, expected):
    """Return module name from initial name, hierarchy folders and modules."""
    assert champollion.parser.guess_module_name(
        name, hierarchy_folders, module_names
    ) == expected
