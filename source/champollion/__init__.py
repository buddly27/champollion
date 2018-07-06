# :coding: utf-8

import os

from ._version import __version__

from .directive.js_data import AutoDataDirective
from .directive.js_function import AutoFunctionDirective
from .directive.js_class import (
    AutoClassDirective, AutoMethodDirective, AutoAttributeDirective
)
from .directive.js_module import AutoModuleDirective

from .viewcode import ViewCode
from .parser import fetch_environment


def setup(app):
    """Register callbacks and directives."""
    app.add_config_value("js_source", None, True)
    app.add_config_value("js_sources", [], True)
    app.add_config_value("js_environment", None, True)
    app.add_config_value("js_class_options", [], True)
    app.add_config_value("js_module_options", [], True)

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
    the path provided via the **js_source** or **js_sources** configuration
    value.

    This function is called with the ``builder-inited`` Sphinx event, emitted
    when the builder object is created.

    .. seealso::

        :ref:`configuration`

    """
    if app.config.js_environment is not None:
        return

    if app.config.js_source is not None:
        path = os.path.abspath(app.config.js_source)
        app.config.js_environment = fetch_environment(path)

    elif len(app.config.js_sources) > 0:
        app.config.js_environment = {}

        for path in app.config.js_sources:
            path = os.path.abspath(path)

            _environment = fetch_environment(path)
            for key in _environment.keys():
                app.config.js_environment.setdefault(key, {})
                app.config.js_environment[key].update(_environment[key])

    else:
        raise RuntimeError(
            "Either the 'js_source' or the 'js_sources' configuration value "
            "must be provided."
        )
