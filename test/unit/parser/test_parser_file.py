# :coding: utf-8

import tempfile
import os

import champollion.parser.file_parser


def test_get_file_environment_empty(request):
    """Return environment from empty file."""
    file_handle, path = tempfile.mkstemp(suffix=".js")
    os.close(file_handle)

    assert champollion.parser.file_parser.get_file_environment(
        path, "path/to/example.js", "test.module"
    ) == {
        "file": {
            "path/to/example.js": {
                "id": "path/to/example.js",
                "module_id": "test.module",
                "name": os.path.basename(path),
                "path": path,
                "content": "",
                "class": {},
                "function": {},
                "data": {}
            }
        },
        "class": {},
        "method": {},
        "attribute": {},
        "function": {},
        "data": {}
    }

    def cleanup():
        """Remove temporary file."""
        try:
            os.remove(path)
        except OSError:
            pass

    request.addfinalizer(cleanup)
    return path


def test_get_file_environment_empty_with_initial_environment(request):
    """Update environment from empty file."""
    file_handle, path = tempfile.mkstemp(suffix=".js")
    os.close(file_handle)

    environment = {
        "module": {
            "test.module": {}
        },
        "class": {
            "test.module.AwesomeClass": {}
        },
        "method": {
            "test.module.AwesomeClass.method": {}
        },
        "attribute": {
            "test.module.AwesomeClass.ATTRIBUTE": {}
        },
        "function": {
            "test.module.doSomething": {}
        },
        "data": {
            "test.module.DATA": {}
        },
        "file": {
            "path/to/other/example.js": {}
        }
    }

    assert champollion.parser.file_parser.get_file_environment(
        path, "path/to/example.js", "test.module", environment
    ) == {
        "file": {
            "path/to/other/example.js": {},
            "path/to/example.js": {
                "id": "path/to/example.js",
                "module_id": "test.module",
                "name": os.path.basename(path),
                "path": path,
                "content": "",
                "class": {},
                "function": {},
                "data": {}
            }
        },
        "module": {
            "test.module": {}
        },
        "class": {
            "test.module.AwesomeClass": {}
        },
        "method": {
            "test.module.AwesomeClass.method": {}
        },
        "attribute": {
            "test.module.AwesomeClass.ATTRIBUTE": {}
        },
        "function": {
            "test.module.doSomething": {}
        },
        "data": {
            "test.module.DATA": {}
        }
    }

    def cleanup():
        """Remove temporary file."""
        try:
            os.remove(path)
        except OSError:
            pass

    request.addfinalizer(cleanup)
    return path
