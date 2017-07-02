# :coding: utf-8

import pytest

import champollion.parser.js_data


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            (
                "/**\n"
                " * test dictionary data.\n"
                " * \n"
                " * Detailed description.\n"
                " */\n"
                "export const DATA = 42;\n"
            ),
            {
                "test.module.DATA": {
                    "id": "test.module.DATA",
                    "module_id": "test.module",
                    "exported": True,
                    "default": False,
                    "name": "DATA",
                    "type": "const",
                    "value": "42",
                    "line_number": 6,
                    "description": (
                        "test dictionary data.\n"
                        "\n"
                        "Detailed description."
                    )
                }
            }
        ),
        (
            (
                "export default var DATA = {\n"
                "   key1: value1,\n"
                "   key2: value2,\n"
                "   key3: value3,\n"
                "};\n"
            ),
            {
                "test.module.DATA": {
                    "id": "test.module.DATA",
                    "module_id": "test.module",
                    "exported": True,
                    "default": True,
                    "name": "DATA",
                    "type": "var",
                    "value": "{ key1: value1, key2: value2, key3: value3, }",
                    "line_number": 1,
                    "description": None
                }
            }
        ),
        (
            (
                "/** test list data */\n"
                "let DATA = [\n"
                "    1, 2, 3 ];\n"
            ),
            {
                "test.module.DATA": {
                    "id": "test.module.DATA",
                    "module_id": "test.module",
                    "exported": False,
                    "default": False,
                    "name": "DATA",
                    "type": "let",
                    "value": "[ 1, 2, 3 ]",
                    "line_number": 2,
                    "description": "test list data"
                }
            }
        ),
        (
            (
                "let DATA = arg =>\n"
                "    console.log(arg);\n"
            ),
            {
                "test.module.DATA": {
                    "id": "test.module.DATA",
                    "module_id": "test.module",
                    "exported": False,
                    "default": False,
                    "name": "DATA",
                    "type": "let",
                    "value": "arg =>console.log(arg)",
                    "line_number": 1,
                    "description": None
                },
            }
        ),
        (
            (
                "const SUM = (arg1, arg2) => {\n"
                "    return arg1 + arg2;\n"
                "};"
            ),
            {
                "test.module.SUM": {
                    "id": "test.module.SUM",
                    "module_id": "test.module",
                    "exported": False,
                    "default": False,
                    "name": "SUM",
                    "type": "const",
                    "value": "(arg1, arg2) => { return arg1 + arg2; }",
                    "line_number": 1,
                    "description": None
                },
            }
        )
    ],
    ids=[
        "valid data",
        "valid object data",
        "valid list data",
        "valid arrow-type function with single argument",
        "valid arrow-type function with severak arguments",
    ]
)
def test_get_data_environment(content, expected):
    """Return data environment from content."""
    assert champollion.parser.js_data.fetch_environment(
        content, "test.module"
    ) == expected


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            "const data_test = 42;",
            {
                "name": "data_test",
                "type": "const",
                "value": "42;",
                "export": None,
                "default": None,
                "start_regex": ""
            }
        ),
        (
            (
                "export let data_test2 = {\n"
                "    key: 'value',\n"
                "};"
            ),
            {
                "name": "data_test2",
                "type": "let",
                "value": (
                    "{\n"
                    "    key: 'value',\n"
                    "};"
                ),
                "export": "export ",
                "default": None,
                "start_regex": ""
            }
        ),
        (
            (
                "var dataTest3 = [\n"
                "    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,\n"
                "];"
            ),
            {
                "name": "dataTest3",
                "type": "var",
                "value": (
                    "[\n"
                    "    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,\n"
                    "];"
                ),
                "export": None,
                "default": None,
                "start_regex": ""
            }
        ),
        (
            "'const attribute = 42'",
            None
        ),
        (
            "const data_test = 42",
            None
        )
    ],
    ids=[
        "valid data",
        "valid object data",
        "valid list data",
        "invalid data string",
        "invalid data with no semi-colons",
    ]
)
def test_data_pattern(content, expected):
    """Match an variable."""
    match = champollion.parser.js_data._DATA_PATTERN.search(
        content
    )
    if expected is None:
        assert match is None
    else:
        assert match.groupdict() == expected
