# :coding: utf-8

import pytest

import champollion.parser.data_element


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
    assert champollion.parser.data_element.fetch_environment(
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


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            "const data_test = 42",
            {
                "name": "data_test",
                "type": "const",
                "value": "42",
                "export": None,
                "default": None,
                "start_regex": ""
            }
        ),
        (
            (
                "export let data_test2 = {\n"
                "    key: 'value',\n"
                "}"
            ),
            {
                "name": "data_test2",
                "type": "let",
                "value": (
                    "{\n"
                    "    key: 'value',\n"
                    "}"
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
                "]"
            ),
            {
                "name": "dataTest3",
                "type": "var",
                "value": (
                    "[\n"
                    "    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,\n"
                    "]"
                ),
                "export": None,
                "default": None,
                "start_regex": ""
            }
        ),
        (
            "'const attribute = 42'",
            None
        )

    ],
    ids=[
        "valid data",
        "valid object data",
        "valid list data",
        "invalid data string",
    ]
)
def test_data_pattern(content, expected):
    """Match an variable."""
    match = champollion.parser.data_element._DATA_PATTERN.search(
        content
    )
    if expected is None:
        assert match is None
    else:
        assert match.groupdict() == expected
