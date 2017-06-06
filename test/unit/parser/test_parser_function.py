# :coding: utf-8

import pytest
import champollion.parser.function_parser


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
        "export default const doSomethingWithManyArguments = ("
        "  arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9"
        ") => {};\n"
        "\n"
        ""
    )


def test_get_function_environment(content):
    """Return function environment from content."""
    assert champollion.parser.function_parser.get_function_environment(
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
