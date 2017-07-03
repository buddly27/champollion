# :coding: utf-8

import pytest

import champollion.parser.js_module


def test_get_module_environment_from_file():
    """Return module_id and environment from file id."""
    assert champollion.parser.js_module.fetch_environment(
        "test/module/example.js", []
    ) == {
        "id": "test.module.example",
        "name": "example",
        "path": "test/module/example",
        "file_id": "test/module/example.js"
    }


def test_get_module_environment_from_index_file():
    """Return module_id and environment from index file id."""
    assert champollion.parser.js_module.fetch_environment(
        "test/module/index.js", []
    ) == {
            "id": "test.module",
            "name": "module",
            "path": "test/module",
            "file_id": "test/module/index.js"
    }


def test_get_module_environment_from_file_with_adjacent_index():
    """Return module_id and environment from file id with adjacent index file.
    """
    assert champollion.parser.js_module.fetch_environment(
        "test/module/example.js", ["index.js"]
    ) == {
        "id": "test.module.example",
        "name": "module.example",
        "path": "test/module/example",
        "file_id": "test/module/example.js"
    }


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
    assert champollion.parser.js_module._guess_module_name(
        name, hierarchy_folders, module_names
    ) == expected
