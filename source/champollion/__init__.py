# :coding: utf-8

import os

from ._version import __version__

from .directive.data_element import AutoDataDirective
from .directive.function_element import AutoFunctionDirective
from .directive.class_element import (
    AutoClassDirective, AutoMethodDirective, AutoAttributeDirective
)
from .directive.module_element import AutoModuleDirective

from .viewcode import ViewCode
from .parser import fetch_environment


def setup(app):
    """Register callbacks and directives."""
    app.add_config_value("js_source", None, True)
    app.add_config_value("js_environment", None, True)
    app.add_config_value("js_class_options", [], True)

    app.connect("builder-inited", fetch_javascript_environment)
    app.connect("doctree-read", ViewCode.add_source_code_links)
    app.connect("html-collect-pages", ViewCode.create_code_pages)
    app.connect("missing-reference", ViewCode.create_missing_code_link)

    app.add_directive_to_domain("js", "autodata", AutoDataDirective)
    app.add_directive_to_domain("js", "autofunction", AutoFunctionDirective)
    app.add_directive_to_domain("js", "autoclass", AutoClassDirective)
    app.add_directive_to_domain("js", "automethod", AutoMethodDirective)
    app.add_directive_to_domain("js", "autoattribute", AutoAttributeDirective)
    app.add_directive_to_domain("js", "automodule", AutoModuleDirective)

    return {
        "version": __version__
    }


def fetch_javascript_environment(app):
    """Fetch the :term:`Javascript` environment from the *app* configuration.

    If the **js_environment** configuration is not provided, attempt to parse
    the path provided via the **js_source** configuration value.

    This function is called with the ``builder-inited`` Sphinx event, emitted
    when the builder object is created.

    """
    if app.config.js_environment is None:
        path = os.path.abspath(app.config.js_source)
        app.config.js_environment = fetch_environment(path)
