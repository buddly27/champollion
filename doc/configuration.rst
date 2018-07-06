.. _configuration:

*******************
Using Configuration
*******************

Some configuration values are available to provide the :term:`Javascript`
source environment or to automatically add options to the :ref:`directives
<directive>`.

These configuration must be added to the
`Sphinx configuration file <http://sphinx-doc.org/config.html>`_.

.. _configuration/js_source:

Using code source
=================

Provide a path to the :term:`Javascript` source code that will be analysed by
:mod:`champollion.parser`::

    # conf.py
    js_source = "/path/to/code"

An environment will be generated when the `builder-inited
<http://www.sphinx-doc.org/en/stable/extdev/appapi.html#event-builder-inited>`_
event is emitted.

It is also possible to provide several paths::

    # conf.py
    js_sources = ["/path/to/code1", "/path/to/code2"]


.. _configuration/js_environment:

Using environment
=================

Provide a :term:`Javascript` environment dictionary which must be in the form of
the :func:`champollion.parser.fetch_environment` returned value::

    # conf.py
    js_environment = {
        "module": {},
        "file": {}
        "class": {},
        "method": {},
        "attribute": {},
        "function": {},
        "data": {}
    }

.. _configuration/js_class_options:

Using autoclass options
=======================

Provide a list of options to apply automatically for all
:ref:`autoclass directives <directive/autoclass>`::

    # conf.py
    js_class_options = ["members", "skip-constructor", "undoc-members"]

This configuration only accept the following boolean options:

* members (When not used as a 'white list')
* skip-constructor
* undoc-members
* private-members
* force-partial-import

.. _configuration/js_module_options:

Using automodule options
========================

Provide a list of options to apply automatically for all
:ref:`automodule directives <directive/automodule>`::

    # conf.py
    js_module_options = ["undoc-members", "private-members"]

This configuration only accept the following boolean options:

* members (When not used as a 'white list')
* skip-description
* undoc-members
* private-members
* force-partial-import
