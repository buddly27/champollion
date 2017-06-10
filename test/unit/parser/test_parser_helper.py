# :coding: utf-8

import pytest

import champollion.parser.helper


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
    assert champollion.parser.helper.get_docstring(
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
    assert champollion.parser.helper.filter_comments(content) == expected


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
    assert champollion.parser.helper.collapse_all(content) == (
        expected_content, expected_collapsed_content
    )


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            "import defaultMember from \"module-name\"",
            {
                "defaultMember": {
                    "id": "defaultMember",
                    "module": "test.module.module-name",
                    "name": "defaultMember",
                    "alias": None,
                    "partial": False
                },
            },
        ),
        (
            (
                "import name1 from \"./module-name1\"\n"
                "import name2 from '../module-name2'\n"
            ),
            {
                "name1": {
                    "id": "name1",
                    "module": "test.module.module-name1",
                    "name": "name1",
                    "alias": None,
                    "partial": False
                },
                "name2": {
                    "id": "name2",
                    "module": "test.module-name2",
                    "name": "name2",
                    "alias": None,
                    "partial": False
                },
            },
        ),
        (
            (
                "import {\n"
                "    name_1 as alias_1,\n"
                "    name_2,\n"
                "    name_3,\n"
                "} from 'module-name'"
            ),
            {
                "alias_1": {
                    "id": "alias_1",
                    "module": "test.module.module-name",
                    "name": "name_1",
                    "alias": "alias_1",
                    "partial": True
                },
                "name_2": {
                    "id": "name_2",
                    "module": "test.module.module-name",
                    "name": "name_2",
                    "alias": None,
                    "partial": True
                },
                "name_3": {
                    "id": "name_3",
                    "module": "test.module.module-name",
                    "name": "name_3",
                    "alias": None,
                    "partial": True
                },
            }
        ),
        (
            (
                "import {name1 as alias1}, name2, {name3} from \"./module\"\n"
            ),
            {
                "alias1": {
                    "id": "alias1",
                    "module": "test.module.module",
                    "name": "name1",
                    "alias": "alias1",
                    "partial": True
                },
                "name2": {
                    "id": "name2",
                    "module": "test.module.module",
                    "name": "name2",
                    "alias": None,
                    "partial": False
                },
                "name3": {
                    "id": "name3",
                    "module": "test.module.module",
                    "name": "name3",
                    "alias": None,
                    "partial": True
                }
            }
        ),
        (
            (
                "import * from 'module1'\n"
                "import * from 'module2'"
            ),
            {
                "WILDCARD_1": {
                    "id": "*",
                    "module": "test.module.module1",
                    "name": "*",
                    "alias": None,
                    "partial": False
                },
                "WILDCARD_2": {
                    "id": "*",
                    "module": "test.module.module2",
                    "name": "*",
                    "alias": None,
                    "partial": False
                }
            }
        ),
        (
            "import * as name from 'module'",
            {
                "name": {
                    "id": "name",
                    "module": "test.module.module",
                    "name": "*",
                    "alias": "name",
                    "partial": False
                }
            }
        )

    ],
    ids=[
        "import default from global module",
        "import default from relative module",
        "import partial on several lines with aliases",
        "import default and partial on several lines with aliases",
        "import wildcard",
        "import wildcard with alias",
    ]
)
def test_get_import_environment(content, expected):
    assert champollion.parser.helper.get_import_environment(
        content, "test.module"
    ) == expected


@pytest.mark.parametrize(
    ("expression", "environment", "wildcards_number", "expected"),
    [
        (
            "name", None, 0,
            (
                {
                    "name": {
                        "id": "name",
                        "module": "test.module",
                        "name": "name",
                        "alias": None,
                        "partial": False
                    }
                },
                0
            )
        ),
        (
            "{name}", None, 0,
            (
                {
                    "name": {
                        "id": "name",
                        "module": "test.module",
                        "name": "name",
                        "alias": None,
                        "partial": True
                    }
                },
                0
            )
        ),
        (
            "{name1 as alias1, name2 as alias2}, name3", None, 1,
            (
                {
                    "alias1": {
                        "id": "alias1",
                        "module": "test.module",
                        "name": "name1",
                        "alias": "alias1",
                        "partial": True
                    },
                    "alias2": {
                        "id": "alias2",
                        "module": "test.module",
                        "name": "name2",
                        "alias": "alias2",
                        "partial": True
                    },
                    "name3": {
                        "id": "name3",
                        "module": "test.module",
                        "name": "name3",
                        "alias": None,
                        "partial": False
                    }
                },
                1
            )
        ),
        (
            "*", None, 0,
            (
                {
                    "WILDCARD_1": {
                        "id": "*",
                        "module": "test.module",
                        "name": "*",
                        "alias": None,
                        "partial": False
                    }
                },
                1
            )
        ),
        (
            "{* as alias}", None, 0,
            (
                {
                    "alias": {
                        "id": "alias",
                        "module": "test.module",
                        "name": "*",
                        "alias": "alias",
                        "partial": True
                    }
                },
                0
            )
        )
    ],
    ids=[
        "simple default expression",
        "simple partial expression",
        "mixed partial and default binding with aliases",
        "wildcard",
        "aliased wildcard"
    ]
)
def test_get_expression_environment(
    expression, environment, wildcards_number, expected
):
    assert champollion.parser.helper.get_expression_environment(
        expression, "test.module", environment, wildcards_number
    ) == expected


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            (
                "/** a description */\n"
                "export {name}"
            ),
            {
                "name": {
                    "id": "name",
                    "name": "name",
                    "module": None,
                    "alias": None,
                    "partial": True,
                    "description": "a description",
                    "default": False,
                    "line_number": 2,
                }
            }
        ),
        (
            (
                "/** a description */\n"
                "export default name"
            ),
            {
                "name": {
                    "id": "name",
                    "name": "name",
                    "module": None,
                    "alias": None,
                    "partial": False,
                    "description": "a description",
                    "default": True,
                    "line_number": 2,
                }
            }
        ),
        (
            (
                "/** a description */\n"
                "export {name as alias}"
            ),
            {
                "alias": {
                    "id": "alias",
                    "name": "name",
                    "module": None,
                    "alias": "alias",
                    "partial": True,
                    "description": "a description",
                    "default": False,
                    "line_number": 2,
                }
            }
        ),
        (
            (
                "/** a description */\n"
                "export {name1 as alias1, name2 as alias2, name3};"
            ),
            {
                "alias1": {
                    "id": "alias1",
                    "name": "name1",
                    "module": None,
                    "alias": "alias1",
                    "partial": True,
                    "description": "a description",
                    "default": False,
                    "line_number": 2,
                },
                "alias2": {
                    "id": "alias2",
                    "name": "name2",
                    "module": None,
                    "alias": "alias2",
                    "partial": True,
                    "description": "a description",
                    "default": False,
                    "line_number": 2,
                },
                "name3": {
                    "id": "name3",
                    "name": "name3",
                    "module": None,
                    "alias": None,
                    "partial": True,
                    "description": "a description",
                    "default": False,
                    "line_number": 2,
                }
            }
        ),
        (
            (
                "/** a description */\n"
                "export name from 'module-name'"
            ),
            {
                "name": {
                    "id": "name",
                    "name": "name",
                    "module": "test.module.module-name",
                    "alias": None,
                    "partial": False,
                    "description": "a description",
                    "default": False,
                    "line_number": 2,
                }
            }
        ),
        (
            (
                "/** a description */\n"
                "export name1 from \"./module-name1\"\n"
                "\n"
                "/** another description */\n"
                "export {name2 as alias2} from '../module-name2'\n"
            ),
            {
                "name1": {
                    "id": "name1",
                    "name": "name1",
                    "module": "test.module.module-name1",
                    "alias": None,
                    "partial": False,
                    "description": "a description",
                    "default": False,
                    "line_number": 2,
                },
                "alias2": {
                    "id": "alias2",
                    "name": "name2",
                    "module": "test.module-name2",
                    "alias": "alias2",
                    "partial": True,
                    "description": "another description",
                    "default": False,
                    "line_number": 5,
                }
            }
        ),
        (
            (
                "export {\n"
                "    name_1 as alias_1,\n"
                "    name_2,\n"
                "    name_3,\n"
                "} from 'module-name'"
            ),
            {
                "alias_1": {
                    "id": "alias_1",
                    "name": "name_1",
                    "module": "test.module.module-name",
                    "alias": "alias_1",
                    "partial": True,
                    "description": None,
                    "default": False,
                    "line_number": 1,
                },
                "name_2": {
                    "id": "name_2",
                    "name": "name_2",
                    "module": "test.module.module-name",
                    "alias": None,
                    "partial": True,
                    "description": None,
                    "default": False,
                    "line_number": 1,
                },
                "name_3": {
                    "id": "name_3",
                    "name": "name_3",
                    "module": "test.module.module-name",
                    "alias": None,
                    "partial": True,
                    "description": None,
                    "default": False,
                    "line_number": 1,
                }
            }
        )
    ],
    ids=[
        "export simple",
        "export default simple",
        "export simple aliased",
        "export several elements with aliased",
        "export default from global module",
        "export default from relative module",
        "export partial on several lines with aliases",
    ]
)
def test_get_export_environment(content, expected):
    assert champollion.parser.helper.get_export_environment(
        content, "test.module"
    ) == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        (
            "name1, name2, name3",
            [
                {
                    "id": "name1",
                    "name": "name1",
                    "alias": None,
                },
                {
                    "id": "name2",
                    "name": "name2",
                    "alias": None,
                },
                {
                    "id": "name3",
                    "name": "name3",
                    "alias": None,
                },
            ]
        ),
        (
            "name as alias",
            [
                {
                    "id": "alias",
                    "name": "name",
                    "alias": "alias",
                }
            ]
        ),
        (
            "name1, * as name2",
            [
                {
                    "id": "name1",
                    "name": "name1",
                    "alias": None,
                },
                {
                    "id": "name2",
                    "name": "*",
                    "alias": "name2",
                }
            ]
        ),
        (
            "name = 42",
            []
        )
    ],
    ids=[
        "three elements",
        "single element with alias",
        "two elements with wildcard",
        "invalid",
    ]
)
def test_get_binding_environment(expression, expected):
    assert champollion.parser.helper.get_binding_environment(
        expression
    ) == expected
