# :coding: utf-8

import os
import shutil
import tempfile
import uuid

import pytest


@pytest.fixture()
def unique_name():
    """Return a unique name."""
    return "unique-{0}".format(uuid.uuid4())


@pytest.fixture()
def temporary_file(request):
    """Return a temporary file path."""
    file_handle, path = tempfile.mkstemp()
    os.close(file_handle)

    def cleanup():
        """Remove temporary file."""
        try:
            os.remove(path)
        except OSError:
            pass

    request.addfinalizer(cleanup)
    return path


@pytest.fixture()
def temporary_directory(request):
    """Return a temporary directory path."""
    path = tempfile.mkdtemp()

    def cleanup():
        """Remove temporary directory."""
        shutil.rmtree(path)

    request.addfinalizer(cleanup)

    return path


@pytest.fixture()
def code_folder():
    return os.path.join(os.path.dirname(__file__), "example")


@pytest.fixture()
def docs_folder(temporary_directory):
    path = os.path.join(temporary_directory, "docs")
    os.makedirs(path)

    # Create minimal conf.py file
    conf_file = os.path.join(path, "conf.py")

    with open(conf_file, "w") as f:
        f.write(
            "# :coding: utf-8\n"
            "extensions=['sphinxcontrib.es6']\n"
            "source_suffix = '.rst'\n"
            "master_doc = 'index'\n"
            "author = u'Jeremy Retailleau'\n"
            "exclude_patterns = ['Thumbs.db', '.DS_Store']\n"
            "js_source='./example'"
        )

    return path

