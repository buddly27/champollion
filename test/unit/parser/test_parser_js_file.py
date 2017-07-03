# :coding: utf-8

import pytest

import tempfile
import os

import champollion.parser.js_file


def test_get_file_environment_empty(request):
    """Return environment from empty file."""
    file_handle, path = tempfile.mkstemp(suffix=".js")
    os.close(file_handle)

    assert champollion.parser.js_file.fetch_environment(
        path, "path/to/example.js", "test.module"
    ) == {
        "id": "path/to/example.js",
        "module_id": "test.module",
        "name": os.path.basename(path),
        "path": path,
        "content": "",
        "description": None,
        "class": {},
        "function": {},
        "data": {},
        "export": {},
        "import": {}
    }

    def cleanup():
        """Remove temporary file."""
        try:
            os.remove(path)
        except OSError:
            pass

    request.addfinalizer(cleanup)
    return path


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            (
                "/**\n"
                " * A file description.\n"
                " * \n"
                " * A detailed description which can be quite long\n"
                " * and eventually go over multiple lines.\n"
                " *\n"
                " * .. note::\n"
                " *\n"
                " *     A note.\n"
                " */\n"
                "\n"
                "function awesomeFunction() {}\n"
                "\n"
            ),
            (
                "A file description.\n"
                "\n"
                "A detailed description which can be quite long\n"
                "and eventually go over multiple lines.\n"
                "\n"
                ".. note::\n"
                "\n"
                "    A note."
            )
        ),
        (
            (
                "/**\n"
                " * A file description.\n"
                " */\n"
                "\n"
                "function awesomeFunction() {}\n"
                "\n"
            ),
            (
                "A file description."
            )
        ),
        (
            (
                "/** A file description. */\n"
                "\n"
                "function awesomeFunction() {}\n"
                "\n"
            ),
            (
                "A file description."
            )
        ),
        (
            (
                "\n"
                "\n// a comment."
                "\n"
                "/** A file description. */\n"
                "\n"
                "function awesomeFunction() {}\n"
                "\n"
            ),
            (
                "A file description."
            )
        ),
        (
            (
                "/* a multi-line comment. */\n"
                "\n"
                "/** A file description. */\n"
                "\n"
                "function awesomeFunction() {}\n"
                "\n"
            ),
            None
        ),
        (
            (
                "/**\n"
                " A file description.\n"
                " \n"
                " A detailed description which can be quite long\n"
                " and eventually go over multiple lines.\n"
                " \n"
                " .. note::\n"
                " \n"
                "     A note.\n"
                "*/\n"
                "\n"
                "function awesomeFunction() {}\n"
                "\n"
            ),
            None
        )
    ],
    ids=[
        "valid description",
        "valid description on three lines",
        "valid description on one line",
        "valid description with top content",
        "invalid description with incorrect top content",
        "invalid description"
    ]
)
def test_fetch_file_description(content, expected):
    assert champollion.parser.js_file.fetch_file_description(
        content
    ) == expected


@pytest.mark.parametrize(
    ("environment", "export_environment", "expected"),
    [
        (
            {
                "id": "__identifier__",
                "description": "A description.",
                "exported": False,
                "default": False
            },
            {},
            {
                "id": "__identifier__",
                "description": "A description.",
                "exported": False,
                "default": False
            }
        ),
        (
            {
                "id": "__identifier__",
                "description": "A description.",
                "exported": False,
                "default": False
            },
            {
                "__identifier__": {
                    "id": "__identifier__",
                    "description": "Another description.",
                    "default": False
                }
            },
            {
                "id": "__identifier__",
                "description": "A description.",
                "exported": True,
                "default": False
            }
        ),
        (
            {
                "id": "__identifier__",
                "description": "A description.",
                "exported": False,
                "default": False
            },
            {
                "__identifier__": {
                    "id": "__identifier__",
                    "description": "Another description.",
                    "default": True
                }
            },
            {
                "id": "__identifier__",
                "description": "A description.",
                "exported": True,
                "default": True
            }
        ),
        (
            {
                "id": "__identifier__",
                "description": None,
                "exported": False,
                "default": False
            },
            {
                "__identifier__": {
                    "id": "__identifier__",
                    "description": "Another description.",
                    "default": False
                }
            },
            {
                "id": "__identifier__",
                "description": "Another description.",
                "exported": True,
                "default": False
            }
        )
    ],
    ids=[
        "empty export environment",
        "update exported environment",
        "update exported default environment",
        "update description from exported environment"
    ]
)
def test_update_from_exported_elements(
    environment, export_environment, expected
):
    """Update environment from exported element."""
    champollion.parser.js_file.update_from_exported_elements(
        environment, export_environment
    )
    assert environment == expected


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            "import defaultMember from \"module-name\"",
            {
                "test.module.defaultMember": {
                    "id": "test.module.defaultMember",
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
                "test.module.name1": {
                    "id": "test.module.name1",
                    "module": "test.module.module-name1",
                    "name": "name1",
                    "alias": None,
                    "partial": False
                },
                "test.module.name2": {
                    "id": "test.module.name2",
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
                "test.module.alias_1": {
                    "id": "test.module.alias_1",
                    "module": "test.module.module-name",
                    "name": "name_1",
                    "alias": "alias_1",
                    "partial": True
                },
                "test.module.name_2": {
                    "id": "test.module.name_2",
                    "module": "test.module.module-name",
                    "name": "name_2",
                    "alias": None,
                    "partial": True
                },
                "test.module.name_3": {
                    "id": "test.module.name_3",
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
                "test.module.alias1": {
                    "id": "test.module.alias1",
                    "module": "test.module.module",
                    "name": "name1",
                    "alias": "alias1",
                    "partial": True
                },
                "test.module.name2": {
                    "id": "test.module.name2",
                    "module": "test.module.module",
                    "name": "name2",
                    "alias": None,
                    "partial": False
                },
                "test.module.name3": {
                    "id": "test.module.name3",
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
                "test.module.WILDCARD_1": {
                    "id": "test.module.WILDCARD_1",
                    "module": "test.module.module1",
                    "name": "*",
                    "alias": None,
                    "partial": False
                },
                "test.module.WILDCARD_2": {
                    "id": "test.module.WILDCARD_2",
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
                "test.module.name": {
                    "id": "test.module.name",
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
def test_fetch_import_environment(content, expected):
    """Return import environment."""
    assert champollion.parser.js_file.fetch_import_environment(
        content, "test.module"
    ) == expected


@pytest.mark.parametrize(
    ("expression", "environment", "wildcards_number", "expected"),
    [
        (
            "name", None, 0,
            (
                {
                    "module.name": {
                        "id": "module.name",
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
                    "module.name": {
                        "id": "module.name",
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
                    "module.alias1": {
                        "id": "module.alias1",
                        "module": "test.module",
                        "name": "name1",
                        "alias": "alias1",
                        "partial": True
                    },
                    "module.alias2": {
                        "id": "module.alias2",
                        "module": "test.module",
                        "name": "name2",
                        "alias": "alias2",
                        "partial": True
                    },
                    "module.name3": {
                        "id": "module.name3",
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
                    "module.WILDCARD_1": {
                        "id": "module.WILDCARD_1",
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
                    "module.alias": {
                        "id": "module.alias",
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
def test_fetch_expression_environment(
    expression, environment, wildcards_number, expected
):
    """Return expression environment."""
    assert champollion.parser.js_file._fetch_expression_environment(
        expression, "module", "test.module", environment, wildcards_number
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
                "test.module.name": {
                    "id": "test.module.name",
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
                "test.module.name": {
                    "id": "test.module.name",
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
                "test.module.alias": {
                    "id": "test.module.alias",
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
                "test.module.alias1": {
                    "id": "test.module.alias1",
                    "name": "name1",
                    "module": None,
                    "alias": "alias1",
                    "partial": True,
                    "description": "a description",
                    "default": False,
                    "line_number": 2,
                },
                "test.module.alias2": {
                    "id": "test.module.alias2",
                    "name": "name2",
                    "module": None,
                    "alias": "alias2",
                    "partial": True,
                    "description": "a description",
                    "default": False,
                    "line_number": 2,
                },
                "test.module.name3": {
                    "id": "test.module.name3",
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
                "test.module.name": {
                    "id": "test.module.name",
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
                "test.module.name1": {
                    "id": "test.module.name1",
                    "name": "name1",
                    "module": "test.module.module-name1",
                    "alias": None,
                    "partial": False,
                    "description": "a description",
                    "default": False,
                    "line_number": 2,
                },
                "test.module.alias2": {
                    "id": "test.module.alias2",
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
                "test.module.alias_1": {
                    "id": "test.module.alias_1",
                    "name": "name_1",
                    "module": "test.module.module-name",
                    "alias": "alias_1",
                    "partial": True,
                    "description": None,
                    "default": False,
                    "line_number": 1,
                },
                "test.module.name_2": {
                    "id": "test.module.name_2",
                    "name": "name_2",
                    "module": "test.module.module-name",
                    "alias": None,
                    "partial": True,
                    "description": None,
                    "default": False,
                    "line_number": 1,
                },
                "test.module.name_3": {
                    "id": "test.module.name_3",
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
def test_fetch_export_environment(content, expected):
    """Return export environment."""
    assert champollion.parser.js_file.fetch_export_environment(
        content, "test.module"
    ) == expected


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        (
            "name;",
            (
                [
                    {
                        "id": "test.module.name",
                        "name": "name",
                        "alias": None,
                    }
                ],
                0
            )
        ),
        (
            "name1, name2, name3",
            (
                [
                    {
                        "id": "test.module.name1",
                        "name": "name1",
                        "alias": None,
                    },
                    {
                        "id": "test.module.name2",
                        "name": "name2",
                        "alias": None,
                    },
                    {
                        "id": "test.module.name3",
                        "name": "name3",
                        "alias": None,
                    },
                ],
                0
            )
        ),
        (
            "name as alias",
            (
                [
                    {
                        "id": "test.module.alias",
                        "name": "name",
                        "alias": "alias",
                    }
                ],
                0
            )

        ),
        (
            "name1, * as name2;",
            (
                [
                    {
                        "id": "test.module.name1",
                        "name": "name1",
                        "alias": None,
                    },
                    {
                        "id": "test.module.name2",
                        "name": "*",
                        "alias": "name2",
                    }
                ],
                0
            )
        ),
        (
            "connect(mapStateToProps, mapDispatchToProps)(ReactComponent)",
            ([], 0)
        ),
        (
            "name = 42",
            ([], 0)
        )
    ],
    ids=[
        "one element",
        "three elements",
        "single element with alias",
        "two elements with wildcard",
        "invalid wrapped element",
        "invalid",
    ]
)
def test_fetch_binding_environment(expression, expected):
    """Return binding environment."""
    assert champollion.parser.js_file._fetch_binding_environment(
        expression, "test.module"
    ) == expected
