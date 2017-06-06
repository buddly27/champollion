# :coding: utf-8

import os

from ._version import __version__

from .directive.data_directive import AutoDataDirective
from .directive.function_directive import AutoFunctionDirective
from .directive.class_directive import AutoClassDirective
from .directive.method_directive import AutoMethodDirective
from .directive.attribute_directive import AutoAttributeDirective
from .directive.module_directive import AutoModuleDirective

from .viewcode import (
    add_source_code_links,
    create_code_pages,
    create_missing_code_link
)
from .parser import get_environment


def parse_js_source(app):
    """Parse the javascript source path and store it in *app* environment.

    This function is called with the ``builder-inited`` Sphinx event, emitted
    when the builder object is created.

    """
    path = os.path.abspath(app.config.js_source)
    app.env.js_environment = get_environment(path)


def setup(app):
    """Register callbacks and directives."""
    app.add_config_value("js_source", None, "env")
    app.add_config_value("js_class_options", [], "env")

    app.connect("builder-inited", parse_js_source)
    app.connect("doctree-read", add_source_code_links)
    app.connect("html-collect-pages", create_code_pages)
    app.connect("missing-reference", create_missing_code_link)

    app.add_directive_to_domain("js", "autodata", AutoDataDirective)
    app.add_directive_to_domain("js", "autofunction", AutoFunctionDirective)
    app.add_directive_to_domain("js", "autoclass", AutoClassDirective)
    app.add_directive_to_domain("js", "automethod", AutoMethodDirective)
    app.add_directive_to_domain("js", "autoattribute", AutoAttributeDirective)
    app.add_directive_to_domain("js", "automodule", AutoModuleDirective)

    return {
        "version": __version__
    }
