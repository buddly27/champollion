# :coding: utf-8

import pytest

import champollion.parser.data_parser


@pytest.fixture()
def content():
    return (
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


def test_get_data_environment(content):
    """Return data environment from content."""
    assert champollion.parser.data_parser.get_data_environment(
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
            "value": "{ key1: value1, key2: value2, key3: value3, }",
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
