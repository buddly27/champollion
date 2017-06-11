# :coding: utf-8

import pytest
import champollion.parser.function_element


@pytest.fixture()
def content():
    return (
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
        "export const doSomethingWithManyArguments = (\n"
        "  arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9\n"
        ") => {};\n"
        "\n"
        "/**\n"
        " * test anonymous function.\n"
        " */\n"
        "export default function (arg1) {\n"
        "    console.log('anonymous function');\n"
        "};\n"
        "\n"
        "/**\n"
        " * test generator function.\n"
        " */\n"
        "function* generate(arg1, arg2) {\n"
        "    yield something();\n"
        "};\n"
    )


def test_get_function_environment(content):
    """Return function environment from content."""
    assert champollion.parser.function_element.fetch_environment(
        content, "test.module"
    ) == {
        "test.module.doSomething": {
            "id": "test.module.doSomething",
            "module_id": "test.module",
            "exported": True,
            "default": False,
            "name": "doSomething",
            "anonymous": False,
            "generator": False,
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
            "anonymous": False,
            "generator": False,
            "arguments": ["arg1", "arg2"],
            "line_number": 9,
            "description": "test function with arguments."
        },
        "test.module.doSomethingWithManyArguments": {
            "id": "test.module.doSomethingWithManyArguments",
            "module_id": "test.module",
            "exported": True,
            "default": False,
            "name": "doSomethingWithManyArguments",
            "anonymous": False,
            "generator": False,
            "arguments": [
                "arg1", "arg2", "arg3", "arg4",
                "arg5", "arg6", "arg7", "arg8",
                "arg9"
            ],
            "line_number": 13,
            "description": None
        },
        "test.module.__ANONYMOUS_FUNCTION__": {
            "id": "test.module.__ANONYMOUS_FUNCTION__",
            "module_id": "test.module",
            "exported": True,
            "default": True,
            "name": "__ANONYMOUS_FUNCTION__",
            "anonymous": True,
            "generator": False,
            "arguments": ["arg1"],
            "line_number": 20,
            "description": "test anonymous function."
        },
        "test.module.generate": {
            "id": "test.module.generate",
            "module_id": "test.module",
            "exported": False,
            "default": False,
            "name": "generate",
            "anonymous": False,
            "generator": True,
            "arguments": ["arg1", "arg2"],
            "line_number": 27,
            "description": "test generator function."
        },
    }


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            "export default function(arg1) {}",
            {
                "arguments": "arg1",
                "data_name": None,
                "default": "default ",
                "export": "export ",
                "function_name": None,
                "generator": None,
                "start_regex": ""
            }
        ),
        (
            "export function doSomething_1() {}",
            {
                "arguments": "",
                "data_name": None,
                "default": None,
                "export": "export ",
                "function_name": "doSomething_1",
                "generator": None,
                "start_regex": ""
            }
        ),
        (
            (
                "function doSomething_Else(\n"
                "    arg1, arg2, arg3, arg3, arg4, arg5,\n"
                ") {\n"
                "    console.log('test')\n"
                "}"
            ),
            {
                "arguments": "arg1, arg2, arg3, arg3, arg4, arg5,",
                "data_name": None,
                "default": None,
                "export": None,
                "function_name": "doSomething_Else",
                "generator": None,
                "start_regex": ""
            }
        ),
        (
            (
                "const aFunction=function saySomething(text) {\n"
                "    console.log(text)\n"
                "}"
            ),
            {
                "arguments": "text",
                "data_name": "aFunction",
                "default": None,
                "export": None,
                "function_name": "saySomething",
                "generator": None,
                "start_regex": ""
            }
        ),
        (
            (
                "let aFunction=function* saySomething(text) {\n"
                "    console.log(text)\n"
                "}"
            ),
            {
                "arguments": "text",
                "data_name": "aFunction",
                "default": None,
                "export": None,
                "function_name": "saySomething",
                "generator": "* ",
                "start_regex": ""
            }
        ),
        (
            (
                "function* saySomething(text) {\n"
                "    console.log(text)\n"
                "}"
            ),
            {
                "arguments": "text",
                "data_name": None,
                "default": None,
                "export": None,
                "function_name": "saySomething",
                "generator": "* ",
                "start_regex": ""
            }
        ),
        (
            "const test = 'const test = function() {}'",
            None
        )
    ],
    ids=[
        "valid anonymous function",
        "valid named function",
        "valid named function with multiple arguments",
        "valid function expression",
        "valid function generator expression",
        "valid function generator",
        "valid function string",
    ]
)
def test_function_pattern(content, expected):
    """Match a function."""
    match = champollion.parser.function_element._FUNCTION_PATTERN.search(content)
    if expected is None:
        assert match is None
    else:
        assert match.groupdict() == expected


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            "const arrow_type_function = (arg1) => {};",
            {
                "arguments": "arg1",
                "single_argument": None,
                "function_name": "arrow_type_function",
                "default": None,
                "export": None,
                "start_regex": ""
            }
        ),
        (
            "let arrow_type_function2 = arg1 => {};",
            {
                "arguments": None,
                "single_argument": "arg1",
                "function_name": "arrow_type_function2",
                "default": None,
                "export": None,
                "start_regex": ""
            }
        ),
        (
            "export const arrow_type_function = (arg1) => {};",
            {
                "arguments": "arg1",
                "single_argument": None,
                "function_name": "arrow_type_function",
                "default": None,
                "export": "export ",
                "start_regex": ""
            }
        ),
        (
            "export default var arrow_type_function3 = (arg1, arg2) => {};",
            {
                "arguments": "arg1, arg2",
                "single_argument": None,
                "function_name": "arrow_type_function3",
                "default": "default ",
                "export": "export ",
                "start_regex": ""
            }
        ),
        (
            (
                "export const arrow_type_function = (\n"
                "    arg1, arg2, arg3, arg4, arg5, agr6,\n"
                ") => {\n"
                "    console.log('youpi');\n"
                "};\n"
            ),
            {
                "arguments": "arg1, arg2, arg3, arg4, arg5, agr6,",
                "single_argument": None,
                "function_name": "arrow_type_function",
                "default": None,
                "export": "export ",
                "start_regex": ""
            }
        ),
        (
            "arrow_type_function = (arg1) => {}",
            None
        ),
        (
            "const test = 'const arrow_type_function = (arg1) => {}'",
            None
        ),
        (
            "(arg1) => {}",
            None
        ),
        (
            "const arrow_type_function = arg1, arg2 => {};",
            None
        ),
    ],
    ids=[
        "valid function with one argument and brackets",
        "valid function with one argument and no brackets",
        "valid exported function",
        "valid function with two arguments",
        "valid function with multiple arguments",
        "invalid arrow-type function without type",
        "invalid arrow-type function string",
        "invalid unassigned arrow-type function",
        "invalid arrow-type function with multiple argument and no brackets",
    ]
)
def test_function_arrow_pattern(content, expected):
    """Match an arrow-type function."""
    match = champollion.parser.function_element._FUNCTION_ARROW_PATTERN.search(
        content
    )
    if expected is None:
        assert match is None
    else:
        assert match.groupdict() == expected
