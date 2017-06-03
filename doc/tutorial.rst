.. _tutorial:

********
Tutorial
********

Once Champollion :ref:`installed <installing>`, add it as an extension to
your `Sphinx configuration file <http://sphinx-doc.org/config.html>`_ and
indicate the path to the :term:`Javascript` source code::

    # conf.py
    extensions = [
        "champollion"
    ]

    js_source="./relative/path/to/example"


Now add one of the :term:`directives <Directive>` available to display the
API documentation to an included source file, such as
:file:`api_reference.rst`.


js:autodata
===========

.. sourcecode:: rest

    .. js:autodata:: example.DATA

js:autofunction
===============

.. sourcecode:: rest

    .. js:autofunction:: example.doSomething

js:autoclass
============

.. sourcecode:: rest

    .. js:autoclass:: example.AwesomeClass

js:automethod
=============

.. sourcecode:: rest

    .. js:autodata:: example.AwesomeClass.myMethod

js:autoattribute
================

.. sourcecode:: rest

    .. js:autodata:: example.AwesomeClass.myAttribute
