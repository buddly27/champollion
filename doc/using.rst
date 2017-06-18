.. _using:

*****
Using
*****

Once Champollion :ref:`installed <installing>`, add it as an extension to
your `Sphinx configuration file <http://sphinx-doc.org/config.html>`_ and
indicate the path to the :term:`Javascript` source code::

    # conf.py
    extensions = [
        "champollion"
    ]

    js_source = "./relative/path/to/example"


All :term:`Javascript` files within the ``js_source`` structure path is parsed
when the sphinx builder is initiated, and all relevant information is fetched
within a configuration environment which includes the description for each
element.

.. seealso::

    :ref:`documenting_javascript`

.. seealso::

    :ref:`configuration`

For all :term:`directives <Directive>`, only **one argument** must be given
which represents the identifier of the element to document. This identifier
depends on the file structure hierarchy.

Let's consider the following example::

    # conf.py
    js_source = "./example"

The identifier of a class named **TestClass** included in
``./example/module/test.js`` will be ``example.module.test.TestClass``. This
class element can be documented as follow:

.. sourcecode:: rest

    *****************************
    example.module.test.TestClass
    *****************************

    .. js:autoclass:: example.module.test.TestClass

.. note::

    Champollion add all :term:`directives <Directive>` to the
    `Javascript domain <http://www.sphinx-doc.org/en/stable/domains.html#the-javascript-domain>`_.
    The ``js:`` prefix must then be used for each directive, or the following
    line should be added to the `Sphinx configuration file
    <http://sphinx-doc.org/config.html>`_::

        # conf.py
        primary_domain = "js"

.. seealso::

    :ref:`directive`
