# :coding: utf-8

import pytest
import os

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
