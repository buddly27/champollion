# :coding: utf-8

"""champollion documentation build configuration file."""

import os
import sys
import re

# -- General ------------------------------------------------------------------

# Inject source onto path so that autodoc can find it by default, but in such a
# way as to allow overriding location.
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source"))
)

# Extensions.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "lowdown"
]


# Add local extension(s).
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "_extension"))
extensions.append("js_reference")

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = u"champollion"
copyright = u"2017, Jeremy Retailleau"

# Version
with open(
    os.path.join(
        os.path.dirname(__file__), "..", "source",
        "champollion", "_version.py"
    )
) as _version_file:
    _version = re.match(
        r".*__version__ = \"(.*?)\"", _version_file.read(), re.DOTALL
    ).group(1)

version = _version
release = _version

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_template"]

# A list of prefixes to ignore for module listings.
modindex_common_prefix = [
    "champollion."
]


# -- HTML output --------------------------------------------------------------

html_theme = "sphinx_rtd_theme"

# If True, copy source rst files to output for reference.
html_copy_source = True


# -- Autodoc ------------------------------------------------------------------

autodoc_default_flags = ["members", "undoc-members"]
autodoc_member_order = "bysource"


# -- Intersphinx --------------------------------------------------------------

intersphinx_mapping = {
    "python": ("http://docs.python.org/", None)
}
