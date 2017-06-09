# :coding: utf-8

import pytest

import champollion.parser.class_parser


@pytest.fixture()
def content():
    return (
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


def test_get_class_environment(content):
    """Return class environment from content."""
    assert champollion.parser.class_parser.get_class_environment(
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


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            "class AwesomeClass",
            None
        ),
        (
            "const test= 'class AwesomeClass {}';",
            None
        ),
        (
            "class AwesomeClass {}",
            {
                "export": None,
                "default": None,
                "class_name": "AwesomeClass",
                "data_name": None,
                "mother_class": None,
            }
        ),
        (
            "class Awesome_Class extends module.Mother-Class{}",
            {
                "export": None,
                "default": None,
                "class_name": "Awesome_Class",
                "data_name": None,
                "mother_class": "module.Mother-Class",
            }
        ),
        (
            "export default class AwesomeClass {}",
            {
                "export": "export ",
                "default": "default ",
                "class_name": "AwesomeClass",
                "data_name": None,
                "mother_class": None,
            }
        ),
        (
            "export const MyClass1= class AwesomeClass {}",
            {
                "export": "export ",
                "default": None,
                "class_name": None,
                "data_name": "MyClass1",
                "mother_class": None,
            }
        ),
        (
            "let MyClass1= class AwesomeClass extends Test2 {}",
            {
                "export": None,
                "default": None,
                "class_name": None,
                "data_name": "MyClass1",
                "mother_class": "Test2",
            }
        ),
    ],
    ids=[
        "invalid class",
        "invalid class string",
        "valid class",
        "valid class with inheritance",
        "valid class exported by default",
        "valid class expression exported",
        "another valid class expression",
    ]
)
def test_class_pattern(content, expected):
    """Match a class."""
    match = champollion.parser.class_parser.CLASS_PATTERN.search(content)
    if expected is None:
        assert match is None
    else:
        assert match.groupdict() == expected


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            "function invalidMethod() {}",
            None
        ),
        (
            "invalidMethod()",
            None
        ),
        (
            "invalidMethod {}",
            None
        ),
        (
            "valid-Method (arg1) {}",
            {
                "arguments": "arg1",
                "method_name": "valid-Method",
                "prefix": None
            }
        ),
        (
            "static valid_method() {}",
            {
                "arguments": "",
                "method_name": "valid_method",
                "prefix": "static "
            }
        ),
        (
            "get valid_method2(){}",
            {
                "arguments": "",
                "method_name": "valid_method2",
                "prefix": "get "
            }
        ),
        (
            (
                "set validMethod( \n"
                "    arg1, arg2, arg3, arg4, arg5,\n"
                "){\n"
                "    console.log('test');\n"
                "}\n"
            ),
            {
                "arguments": "arg1, arg2, arg3, arg4, arg5,",
                "method_name": "validMethod",
                "prefix": "set "
            }
        ),
    ],
    ids=[
        "invalid method with 'function' statement",
        "invalid method without nested element",
        "invalid method without argument",
        "valid method",
        "valid static method",
        "valid getter method",
        "valid setter method",
    ]
)
def test_class_method_pattern(content, expected):
    """Match a class method."""
    match = champollion.parser.class_parser.CLASS_METHOD_PATTERN.search(content)
    if expected is None:
        assert match is None
    else:
        assert match.groupdict() == expected
