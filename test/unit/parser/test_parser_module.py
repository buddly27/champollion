# :coding: utf-8

import pytest

import champollion.parser.module_parser


def test_get_module_environment_from_file():
    """Return module_id and environment from file id."""
    assert champollion.parser.module_parser.get_module_environment(
        "test/module/example.js", []
    ) == (
        "test.module.example",
        {
            "module": {
                "test.module.example": {
                    "id": "test.module.example",
                    "name": "example",
                    "file_id": "test/module/example.js"
                }
            }
        }
    )


def test_get_module_environment_from_index_file():
    """Return module_id and environment from index file id."""
    assert champollion.parser.get_module_environment(
        "test/module/index.js", []
    ) == (
        "test.module",
        {
            "module": {
                "test.module": {
                    "id": "test.module",
                    "name": "module",
                    "file_id": "test/module/index.js"
                }
            }
        }
    )


def test_get_module_environment_from_file_with_adjacent_index():
    """Return module_id and environment from file id with adjacent index file.
    """
    assert champollion.parser.get_module_environment(
        "test/module/example.js", ["index.js"]
    ) == (
        "test.module.example",
        {
            "module": {
                "test.module.example": {
                    "id": "test.module.example",
                    "name": "module.example",
                    "file_id": "test/module/example.js"
                }
            }
        }
    )


def test_get_module_environment_from_file_with_initial_environment():
    """Return module_id and updated environment from file id and module id."""
    environment = {
        "module": {
            "test": {}
        },
        "class": {
            "test.AwesomeClass": {}
        },
        "function": {
            "test.doSomething": {}
        },
        "data": {
            "test.DATA": {}
        },
        "file": {
            "path/to/other/example.js": {}
        }
    }

    assert champollion.parser.get_module_environment(
        "test/module/index.js", [], environment
    ) == (
        "test.module",
        {
            "module": {
                "test": {},
                "test.module": {
                    "id": "test.module",
                    "name": "test.module",
                    "file_id": "test/module/index.js"
                }
            },
            "file": {
                "path/to/other/example.js": {}
            },
            "class": {
                "test.AwesomeClass": {}
            },
            "function": {
                "test.doSomething": {}
            },
            "data": {
                "test.DATA": {}
            }
        }
    )


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
    assert champollion.parser.module_parser.guess_module_name(
        name, hierarchy_folders, module_names
    ) == expected
