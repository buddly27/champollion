# :coding: utf-8

import os
import shutil
import tempfile

import pytest


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
def doc_folder(temporary_directory):
    path = os.path.join(temporary_directory, "doc")
    os.makedirs(path)

    # Create the js code source folder
    js_source = os.path.join(temporary_directory, "doc", "example")
    os.makedirs(js_source)

    # Create minimal conf.py file
    conf_file = os.path.join(path, "conf.py")

    with open(conf_file, "w") as f:
        f.write(
            "# :coding: utf-8\n"
            "extensions=['champollion']\n"
            "source_suffix = '.rst'\n"
            "master_doc = 'index'\n"
            "author = u'Jeremy Retailleau'\n"
            "exclude_patterns = ['Thumbs.db', '.DS_Store']\n"
            "js_source='./example'"
        )

    return path


# @pytest.fixture()
# def doc_folder():
#     temporary_directory = "/var/tmp"
#     path = os.path.join(temporary_directory, "doc")
#     os.makedirs(path)
#
#     # Create the js code source folder
#     js_source = os.path.join(temporary_directory, "doc", "example")
#     os.makedirs(js_source)
#
#     # Create minimal conf.py file
#     conf_file = os.path.join(path, "conf.py")
#
#     with open(conf_file, "w") as f:
#         f.write(
#             "# :coding: utf-8\n"
#             "extensions=['champollion']\n"
#             "html_theme = 'sphinx_rtd_theme'\n"
#             "source_suffix = '.rst'\n"
#             "master_doc = 'index'\n"
#             "author = u'Jeremy Retailleau'\n"
#             "exclude_patterns = ['Thumbs.db', '.DS_Store']\n"
#             "js_source='./example'"
#         )
#
#     return path
