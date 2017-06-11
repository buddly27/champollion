# :coding: utf-8

import pytest

import champollion.parser.class_element


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
        "     * An awesome method.\n"
        "     */\n"
        "    awesomeMethod(arg1, arg2) {\n"
        "        console.log('Method has been called');\n"
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
        "     * A first arrow-type method.\n"
        "     */\n"
        "    anArrowType_method1 = (arg1, arg2 = true) => {\n"
        "        console.log('test1');\n"
        "    };\n"
        "\n"
        "\n"
        "    /**\n"
        "     * A second arrow-type method.\n"
        "     */\n"
        "    anArrowType_method2 = arg => {\n"
        "        console.log('test2');\n"
        "    };\n"
        "\n"
        "    /**\n"
        "     * A static attribute.\n"
        "     */\n"
        "    static attribute1 = 42;\n"
        "\n"
        "    /**\n"
        "     * An object attribute.\n"
        "     */\n"
        "    attribute2 = {\n"
        "        key1: 'value1',\n"
        "        key2: 'value2',\n"
        "    };\n"
        "\n"
        "    /**\n"
        "     * A list attribute.\n"
        "     */\n"
        "    attribute3 = [\n"
        "        'value1',\n"
        "        'value2',\n"
        "    ]\n"
        "}\n"
    )


def test_get_class_environment(content):
    """Return class environment from content."""
    assert champollion.parser.class_element.fetch_environment(
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
                "test.module.AwesomeClass.awesomeMethod": {
                    "id": "test.module.AwesomeClass.awesomeMethod",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "awesomeMethod",
                    "prefix": None,
                    "arguments": ["arg1", "arg2"],
                    "line_number": 51,
                    "description": "An awesome method."
                },
                "test.module.AwesomeClass.staticMethod": {
                    "id": "test.module.AwesomeClass.staticMethod",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "staticMethod",
                    "prefix": "static",
                    "arguments": [],
                    "line_number": 58,
                    "description": "A static method."
                },
                "test.module.AwesomeClass.anArrowType_method1": {
                    "id": "test.module.AwesomeClass.anArrowType_method1",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "anArrowType_method1",
                    "prefix": None,
                    "arguments": ["arg1", "arg2 = true"],
                    "line_number": 65,
                    "description": "A first arrow-type method."
                },
                "test.module.AwesomeClass.anArrowType_method2": {
                    "id": "test.module.AwesomeClass.anArrowType_method2",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "anArrowType_method2",
                    "prefix": None,
                    "arguments": ["arg"],
                    "line_number": 73,
                    "description": "A second arrow-type method."
                },
            },
            "attribute": {
                "test.module.AwesomeClass.attribute1": {
                    "id": "test.module.AwesomeClass.attribute1",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "attribute1",
                    "prefix": "static",
                    "value": "42",
                    "line_number": 80,
                    "description": "A static attribute."
                },
                "test.module.AwesomeClass.attribute2": {
                    "id": "test.module.AwesomeClass.attribute2",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "attribute2",
                    "prefix": None,
                    "value": (
                        "{\n"
                        "        key1: 'value1',\n"
                        "        key2: 'value2',\n"
                        "    }"
                    ),
                    "line_number": 85,
                    "description": "An object attribute."
                },
                "test.module.AwesomeClass.attribute3": {
                    "id": "test.module.AwesomeClass.attribute3",
                    "class_id": "test.module.AwesomeClass",
                    "module_id": "test.module",
                    "name": "attribute3",
                    "prefix": None,
                    "value": (
                        "[\n"
                        "        'value1',\n"
                        "        'value2',\n"
                        "    ]"
                    ),
                    "line_number": 93,
                    "description": "A list attribute."
                },
                "test.module.AwesomeClass.anArrowType_method1": {
                    "description": "A first arrow-type method.",
                    "class_id": "test.module.AwesomeClass",
                    "id": "test.module.AwesomeClass.anArrowType_method1",
                    "line_number": 65,
                    "module_id": "test.module",
                    "name": "anArrowType_method1",
                    "prefix": None,
                    "value": (
                        "(arg1, arg2 = true) => {\n"
                        "        console.log('test1');\n"
                        "    }"
                    ),
                },
                "test.module.AwesomeClass.anArrowType_method2": {
                    "description": "A second arrow-type method.",
                    "class_id": "test.module.AwesomeClass",
                    "id": "test.module.AwesomeClass.anArrowType_method2",
                    "line_number": 73,
                    "module_id": "test.module",
                    "name": "anArrowType_method2",
                    "prefix": None,
                    "value": (
                        "arg => {\n"
                        "        console.log('test2');\n"
                        "    }"
                    ),
                },
            },
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
                "start_regex": ""
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
                "start_regex": ""
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
                "start_regex": ""
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
                "start_regex": ""
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
                "start_regex": ""
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
    match = champollion.parser.class_element._CLASS_PATTERN.search(content)
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
                "prefix": None,
                "start_regex": ""
            }
        ),
        (
            "static valid_method() {}",
            {
                "arguments": "",
                "method_name": "valid_method",
                "prefix": "static ",
                "start_regex": ""
            }
        ),
        (
            "get valid_method2(){}",
            {
                "arguments": "",
                "method_name": "valid_method2",
                "prefix": "get ",
                "start_regex": ""
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
                "prefix": "set ",
                "start_regex": ""
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
    match = champollion.parser.class_element._CLASS_METHOD_PATTERN.search(
        content
    )
    if expected is None:
        assert match is None
    else:
        assert match.groupdict() == expected


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            "arrow_type_method = (arg1) => {};",
            {
                "arguments": "arg1",
                "single_argument": None,
                "method_name": "arrow_type_method",
                "prefix": None,
                "start_regex": ""
            }
        ),
        (
            "arrow_type_method2 = arg1 => {};",
            {
                "arguments": None,
                "single_argument": "arg1",
                "method_name": "arrow_type_method2",
                "prefix": None,
                "start_regex": ""
            }
        ),
        (
            "static arrow_type_method = (arg1) => {};",
            {
                "arguments": "arg1",
                "single_argument": None,
                "method_name": "arrow_type_method",
                "prefix": "static ",
                "start_regex": ""
            }
        ),
        (
            "arrow_type_method3 = (arg1, arg2) => {};",
            {
                "arguments": "arg1, arg2",
                "single_argument": None,
                "method_name": "arrow_type_method3",
                "prefix": None,
                "start_regex": ""
            }
        ),
        (
            (
                "arrow_type_method3 = (\n"
                "    arg1, arg2, arg3, arg4, arg5, agr6,\n"
                ") => {\n"
                "    console.log('youpi');\n"
                "};\n"
            ),
            {
                "arguments": "arg1, arg2, arg3, arg4, arg5, agr6,",
                "single_argument": None,
                "method_name": "arrow_type_method3",
                "prefix": None,
                "start_regex": ""
            }
        ),
        (
            "const arrow_type_method = (arg1) => {}",
            None
        ),
        (
            "const test = 'arrow_type_method = (arg1) => {}'",
            None
        ),
        (
            "(arg1) => {}",
            None
        ),
        (
            "const arrow_type_method = arg1, arg2 => {};",
            None
        ),
    ],
    ids=[
        "valid method with one argument and brackets",
        "valid method with one argument and no brackets",
        "valid static method",
        "valid method with two arguments",
        "valid method with multiple arguments",
        "invalid arrow-type method with type",
        "invalid arrow-type method string",
        "invalid unassigned arrow-type method",
        "invalid arrow-type method with multiple argument and no brackets",
    ]
)
def test_class_method_arrow_pattern(content, expected):
    """Match a class arrow-type method."""
    match = champollion.parser.class_element._CLASS_METHOD_ARROW_PATTERN.search(
        content
    )
    if expected is None:
        assert match is None
    else:
        assert match.groupdict() == expected


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            "attribute_test1 = 42",
            {
                "name": "attribute_test1",
                "value": "42",
                "prefix": None,
                "start_regex": ""
            }
        ),
        (
            (
                "static attribute_test2 = {\n"
                "    key: 'value',\n"
                "}"
            ),
            {
                "name": "attribute_test2",
                "value": (
                    "{\n"
                    "    key: 'value',\n"
                    "}"
                ),
                "prefix": "static ",
                "start_regex": ""
            }
        ),
        (
            (
                "attribute_test3 = [\n"
                "    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,\n"
                "]"
            ),
            {
                "name": "attribute_test3",
                "value": (
                    "[\n"
                    "    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,\n"
                    "]"
                ),
                "prefix": None,
                "start_regex": ""
            }
        ),
        (
            "const test = 'static attribute = 42'",
            None
        )

    ],
    ids=[
        "valid attribute",
        "valid static object attribute",
        "valid static object attribute",
        "invalid attribute string",
    ]
)
def test_class_attribute_pattern(content, expected):
    """Match a class attribute."""
    match = champollion.parser.class_element._CLASS_ATTRIBUTE_PATTERN.search(
        content
    )
    if expected is None:
        assert match is None
    else:
        assert match.groupdict() == expected
