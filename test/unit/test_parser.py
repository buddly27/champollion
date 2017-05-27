# :coding: utf-8

import pytest

import sphinxcontrib.parser


def test_parse_repository_error():
    """Raise an error if the path is incorrect."""
    with pytest.raises(OSError):
        sphinxcontrib.parser.parse_repository("")


def test_parse_repository_empty(temporary_directory):
    """Raise an empty environment."""
    environment = dict(
        modules={},
        classes={},
        functions={},
        variables={},
        files={}
    )
    assert sphinxcontrib.parser.parse_repository(
        temporary_directory
    ) == environment


@pytest.fixture()
def content_lines_with_docstrings():
    return [
        "/**",
        " * An function example.",
        " *",
        " * Detailed description.",
        " */",
        "function sum(a, b) {",
        "    return a+b;",
        "}",
        "",
        "/*",
        " * Incorrect docstring",
        " */",
        "function doSomething() {",
        "    console.log('something');",
        "}",
        "",
        "/*",
        "",
        " Incorrect docstring",
        "",
        "*/",
        "function doSomethingElse() {",
        "    console.log('something_else');",
        "}",
        "",
        "",
        "/* A cool variable. */",
        "const Data = null",
    ]


@pytest.mark.parametrize(
    ("content_lines", "line_number", "expected"),
    [
        (
            [
                "/**",
                " * An function example.",
                " *",
                " * Detailed description.",
                " */",
                "function sum(a, b) {",
                "    return a+b;",
                "}",
            ],
            6,
            (
                "An function example.\n"
                "\n"
                "Detailed description."
            )
        ),
        (
            [
                "/** A cool variable. */",
                "const Data = null",
            ],
            2,
            (
                "A cool variable."
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
                "/** A cool variable. */",
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
def test_parse_docstrings(content_lines, line_number, expected):
    """Return docstrings from a element's line number."""
    assert sphinxcontrib.parser.parse_docstring(
        line_number, content_lines
    ) == expected


def test_filter_comments():
    """Remove all comments from content"""
    content = (
        "'use strict' /* a beautiful comment */\n"
        "\n"
        "/*\n"
        "a long comment that can take a lot of places so\n"
        "we put it on several lines.\n"
        "*/\n"
        "\n"
        "// a variable docstring\n"
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
        "'use strict' \n"
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
    assert sphinxcontrib.parser.filter_comments(content) == expected


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            "const emptyObject = {};",
            "const emptyObject = {};",
        ),
        (
            "let test = {a: 1, b: 2, c: 3};",
            "let test = {};"
        ),
        (
            (
                "const element = {"
                "    key1: value1,"
                "    key2: value2,"
                "    key3: value3,"
                "};"
                ""
                "function sum(a, b) {"
                "    return a+b"
                "}"
                ""
            ),
            (
                "const element = {}"
                ""
                ""
                ""
                ";"
                ""
                "function sum(a, b) {}"
                ""
                ""
                ""
            )
        ),
        (
            (
                "class AwesomeClass {"
                "    constructor() {"
                "        this.variable = 1;"
                "    }"
                ""
                "    increase() {"
                "        this.variable += 1;"
                "    }"
                "}"
            ),
            (
                "class AwesomeClass {}"
                ""
                ""
                ""
                ""
                ""
                ""
                ""
                ""
            )
        )
    ],
    ids=[
        "empty object",
        "simple object",
        "objects and functions on multiple lines",
        "nested class"
    ]
)
def test_collapse_all(content, expected):
    """Collapse all objects, classes and functions."""
    assert sphinxcontrib.parser.collapse_all(content) == expected


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
    assert sphinxcontrib.parser.guess_module_name(
        name, hierarchy_folders, module_names
    ) == expected
