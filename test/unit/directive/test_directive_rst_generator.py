# :coding: utf-8

import pytest

import champollion.directive.rst_generator
from docutils.statemachine import StringList


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (
            {
                "whitelist_names": None,
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test.Class1",
                            "    :alias: Class1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test.Class4",
                            "    :alias: Class4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": ["Class1"],
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test.Class1",
                            "    :alias: Class1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "undocumented_members": True,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test.Class1",
                            "    :alias: Class1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                8: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test.Class2",
                            "    :alias: Class2",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test.Class4",
                            "    :alias: Class4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "undocumented_members": False,
                "private_members": True,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test.Class1",
                            "    :alias: Class1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                16: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test._Class3",
                            "    :alias: _Class3",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test.Class4",
                            "    :alias: Class4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": True,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test.Class1",
                            "    :alias: Class1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "    :force-partial-import:",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test.Class4",
                            "    :alias: Class4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "    :force-partial-import:",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": {
                    42: [
                        StringList(
                            [
                                "",
                                ".. js:autoclass:: example.Test",
                                "    :alias: Test",
                                "    :module-alias: example",
                                "    :module-path-alias: example",
                                "",
                                ""
                            ]
                        )
                    ]
                }
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test.Class1",
                            "    :alias: Class1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: test.Class4",
                            "    :alias: Class4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                42: [
                    StringList(
                        [
                            "",
                            ".. js:autoclass:: example.Test",
                            "    :alias: Test",
                            "    :module-alias: example",
                            "    :module-path-alias: example",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
    ],
    ids=[
        "no options",
        "with whitelist names",
        "with undocumented members",
        "with private members",
        "with force-partial-import option",
        "with initial RST elements"
    ]
)
def test_get_rst_class_elements(options, expected):
    """Generate reStructuredText dictionary from class environment.
    """
    environment = {
        "class": {
            "test.Class1": {
                "id": "test.Class1",
                "name": "Class1",
                "description": "A super class\n\n.. note:: A note.",
                "line_number": 2
            },
            "test.Class2": {
                "id": "test.Class2",
                "name": "Class2",
                "description": None,
                "line_number": 8
            },
            "test._Class3": {
                "id": "test._Class3",
                "name": "_Class3",
                "description": "A private class\n\n.. note:: A note.",
                "line_number": 16
            },
            "test.Class4": {
                "id": "test.Class4",
                "name": "Class4",
                "description": "An interesting class\n\n.. note:: A note.",
                "line_number": 25
            },
        }
    }

    assert champollion.directive.rst_generator.get_rst_class_elements(
        environment, "test.module", "test/module", **options
    ) == expected


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (
            {
                "whitelist_names": None,
                "blacklist_ids": None,
                "undocumented_members": False,
                "private_members": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: test.Class.attribute1",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: test.Class.attribute4",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": ["attribute1"],
                "blacklist_ids": None,
                "undocumented_members": False,
                "private_members": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: test.Class.attribute1",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "blacklist_ids": ["test.Class.attribute1"],
                "undocumented_members": False,
                "private_members": False,
                "rst_elements": None,
            },
            {
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: test.Class.attribute4",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "blacklist_ids": None,
                "undocumented_members": True,
                "private_members": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: test.Class.attribute1",
                            "",
                            ""
                        ]
                    )
                ],
                8: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: test.Class.attribute2",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: test.Class.attribute4",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "blacklist_ids": None,
                "undocumented_members": False,
                "private_members": True,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: test.Class.attribute1",
                            "",
                            ""
                        ]
                    )
                ],
                16: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: test.Class._attribute3",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: test.Class.attribute4",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "blacklist_ids": None,
                "undocumented_members": False,
                "private_members": False,
                "rst_elements": {
                    42: [
                        StringList(
                            [
                                "",
                                ".. js:autoattribute:: example.Test.attribute",
                                "",
                                ""
                            ]
                        )
                    ]
                }
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: test.Class.attribute1",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: test.Class.attribute4",
                            "",
                            ""
                        ]
                    )
                ],
                42: [
                    StringList(
                        [
                            "",
                            ".. js:autoattribute:: example.Test.attribute",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
    ],
    ids=[
        "no options",
        "with whitelist names",
        "with blacklist ids",
        "with undocumented members",
        "with private members",
        "with initial RST elements"
    ]
)
def test_get_rst_attribute_elements(options, expected):
    """Generate reStructuredText dictionary from class attribute environment.
    """
    class_environment = {
        "attribute": {
            "test.Class.attribute1": {
                "id": "test.Class.attribute1",
                "name": "attribute1",
                "description": "A super attribute\n\n.. note:: A note.",
                "line_number": 2
            },
            "test.Class.attribute2": {
                "id": "test.Class.attribute2",
                "name": "attribute2",
                "description": None,
                "line_number": 8
            },
            "test.Class._attribute3": {
                "id": "test.Class._attribute3",
                "name": "_attribute3",
                "description": "A private attribute\n\n.. note:: A note.",
                "line_number": 16
            },
            "test.Class.attribute4": {
                "id": "test.Class.attribute4",
                "name": "attribute4",
                "description": "An interesting attribute\n\n.. note:: A note.",
                "line_number": 25
            },
        }
    }

    assert champollion.directive.rst_generator.get_rst_attribute_elements(
        class_environment, **options
    ) == expected


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (
            {
                "whitelist_names": None,
                "skip_constructor": False,
                "undocumented_members": False,
                "private_members": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: test.Class.method1",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: test.Class.constructor",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": ["method1"],
                "skip_constructor": False,
                "undocumented_members": False,
                "private_members": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: test.Class.method1",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "skip_constructor": True,
                "undocumented_members": False,
                "private_members": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: test.Class.method1",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "skip_constructor": False,
                "undocumented_members": True,
                "private_members": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: test.Class.method1",
                            "",
                            ""
                        ]
                    )
                ],
                8: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: test.Class.method2",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: test.Class.constructor",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "skip_constructor": False,
                "undocumented_members": False,
                "private_members": True,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: test.Class.method1",
                            "",
                            ""
                        ]
                    )
                ],
                16: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: test.Class._method3",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: test.Class.constructor",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "skip_constructor": False,
                "undocumented_members": False,
                "private_members": False,
                "rst_elements": {
                    42: [
                        StringList(
                            [
                                "",
                                ".. js:automethod:: example.Test.method",
                                "",
                                ""
                            ]
                        )
                    ]
                }
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: test.Class.method1",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: test.Class.constructor",
                            "",
                            ""
                        ]
                    )
                ],
                42: [
                    StringList(
                        [
                            "",
                            ".. js:automethod:: example.Test.method",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
    ],
    ids=[
        "no options",
        "with whitelist names",
        "with constructor skipped",
        "with undocumented members",
        "with private members",
        "with initial RST elements"
    ]
)
def test_get_rst_method_elements(options, expected):
    """Generate reStructuredText dictionary from class method environment.
    """
    class_environment = {
        "method": {
            "test.Class.method1": {
                "id": "test.Class.method1",
                "name": "method1",
                "description": "A super method\n\n.. note:: A note.",
                "line_number": 2
            },
            "test.Class.method2": {
                "id": "test.Class.method2",
                "name": "method2",
                "description": None,
                "line_number": 8
            },
            "test.Class._method3": {
                "id": "test.Class._method3",
                "name": "_method3",
                "description": "A private method\n\n.. note:: A note.",
                "line_number": 16
            },
            "test.Class.constructor": {
                "id": "test.Class.constructor",
                "name": "constructor",
                "description": "A constructor.",
                "line_number": 25
            },
        }
    }

    assert champollion.directive.rst_generator.get_rst_method_elements(
        class_environment, **options
    ) == expected


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (
            {
                "whitelist_names": None,
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test.function1",
                            "    :alias: function1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test.function4",
                            "    :alias: function4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": ["function1"],
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test.function1",
                            "    :alias: function1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "undocumented_members": True,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test.function1",
                            "    :alias: function1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                8: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test.function2",
                            "    :alias: function2",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test.function4",
                            "    :alias: function4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "undocumented_members": False,
                "private_members": True,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test.function1",
                            "    :alias: function1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                16: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test._function3",
                            "    :alias: _function3",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test.function4",
                            "    :alias: function4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": True,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test.function1",
                            "    :alias: function1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "    :force-partial-import:",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test.function4",
                            "    :alias: function4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "    :force-partial-import:",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": {
                    42: [
                        StringList(
                            [
                                "",
                                ".. js:autofunction:: example.test",
                                "    :alias: test",
                                "    :module-alias: example",
                                "    :module-path-alias: example",
                                "",
                                ""
                            ]
                        )
                    ]
                }
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test.function1",
                            "    :alias: function1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: test.function4",
                            "    :alias: function4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                42: [
                    StringList(
                        [
                            "",
                            ".. js:autofunction:: example.test",
                            "    :alias: test",
                            "    :module-alias: example",
                            "    :module-path-alias: example",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
    ],
    ids=[
        "no options",
        "with whitelist names",
        "with undocumented members",
        "with private members",
        "with force-partial-import option",
        "with initial RST elements"
    ]
)
def test_get_rst_function_elements(options, expected):
    """Generate reStructuredText dictionary from function environment.
    """
    environment = {
        "function": {
            "test.function1": {
                "id": "test.function1",
                "name": "function1",
                "description": "A super function\n\n.. note:: A note.",
                "line_number": 2
            },
            "test.function2": {
                "id": "test.function2",
                "name": "function2",
                "description": None,
                "line_number": 8
            },
            "test._function3": {
                "id": "test._function3",
                "name": "_function3",
                "description": "A private function\n\n.. note:: A note.",
                "line_number": 16
            },
            "test.function4": {
                "id": "test.function4",
                "name": "function4",
                "description": "An interesting function\n\n.. note:: A note.",
                "line_number": 25
            },
        }
    }

    assert champollion.directive.rst_generator.get_rst_function_elements(
        environment, "test.module", "test/module", **options
    ) == expected


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        (
            {
                "whitelist_names": None,
                "blacklist_ids": None,
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA1",
                            "    :alias: DATA1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA4",
                            "    :alias: DATA4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": ["DATA1"],
                "blacklist_ids": None,
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA1",
                            "    :alias: DATA1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "blacklist_ids": ["test.DATA1"],
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA4",
                            "    :alias: DATA4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "blacklist_ids": None,
                "undocumented_members": True,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA1",
                            "    :alias: DATA1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                8: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA2",
                            "    :alias: DATA2",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA4",
                            "    :alias: DATA4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "blacklist_ids": None,
                "undocumented_members": False,
                "private_members": True,
                "force_partial_import": False,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA1",
                            "    :alias: DATA1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                16: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test._DATA3",
                            "    :alias: _DATA3",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA4",
                            "    :alias: DATA4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "blacklist_ids": None,
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": True,
                "rst_elements": None,
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA1",
                            "    :alias: DATA1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "    :force-partial-import:",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA4",
                            "    :alias: DATA4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "    :force-partial-import:",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
        (
            {
                "whitelist_names": None,
                "blacklist_ids": None,
                "undocumented_members": False,
                "private_members": False,
                "force_partial_import": False,
                "rst_elements": {
                    42: [
                        StringList(
                            [
                                "",
                                ".. js:autodata:: example.TEST",
                                "    :alias: TEST",
                                "    :module-alias: example",
                                "    :module-path-alias: example",
                                "",
                                ""
                            ]
                        )
                    ]
                }
            },
            {
                2: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA1",
                            "    :alias: DATA1",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                25: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: test.DATA4",
                            "    :alias: DATA4",
                            "    :module-alias: test.module",
                            "    :module-path-alias: test/module",
                            "",
                            ""
                        ]
                    )
                ],
                42: [
                    StringList(
                        [
                            "",
                            ".. js:autodata:: example.TEST",
                            "    :alias: TEST",
                            "    :module-alias: example",
                            "    :module-path-alias: example",
                            "",
                            ""
                        ]
                    )
                ]
            }
        ),
    ],
    ids=[
        "no options",
        "with whitelist names",
        "with blacklist ids",
        "with undocumented members",
        "with private members",
        "with force-partial-import option",
        "with initial RST elements"
    ]
)
def test_get_rst_data_elements(options, expected):
    """Generate reStructuredText dictionary from data environment.
    """
    environment = {
        "data": {
            "test.DATA1": {
                "id": "test.DATA1",
                "name": "DATA1",
                "description": "A super data\n\n.. note:: A note.",
                "line_number": 2
            },
            "test.DATA2": {
                "id": "test.DATA2",
                "name": "DATA2",
                "description": None,
                "line_number": 8
            },
            "test._DATA3": {
                "id": "test._DATA3",
                "name": "_DATA3",
                "description": "A private data\n\n.. note:: A note.",
                "line_number": 16
            },
            "test.DATA4": {
                "id": "test.DATA4",
                "name": "DATA4",
                "description": "An interesting data\n\n.. note:: A note.",
                "line_number": 25
            },
        }
    }

    assert champollion.directive.rst_generator.get_rst_data_elements(
        environment, "test.module", "test/module", **options
    ) == expected
