# :coding: utf-8

import os

from ._version import __version__

from directive import (
    AutoDataDirective,
    AutoFunctionDirective,
    AutoClassDirective
)
from viewcode import (
    add_source_code_links,
    create_code_pages,
    create_missing_code_link
)
import parser


def parse_js_source(app):
    """Parse the javascript source path."""
    path = os.path.abspath(app.config.js_source)
    app.env.js_environment = parser.get_environment(path)


def setup(app):
    """Register the javascript autodoc directives."""
    app.add_config_value("js_source", None, "env")

    app.connect("builder-inited", parse_js_source)
    app.connect("doctree-read", add_source_code_links)
    app.connect("html-collect-pages", create_code_pages)
    app.connect("missing-reference", create_missing_code_link)

    app.add_directive_to_domain("js", "autodata", AutoDataDirective)
    app.add_directive_to_domain("js", "autofunction", AutoFunctionDirective)
    app.add_directive_to_domain("js", "autoclass", AutoClassDirective)
    # app.add_directive_to_domain("js", "automodule", AutoModuleDirective)
