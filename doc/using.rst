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

    js_source="./relative/path/to/example"


Parsing the Source code
=======================

All :term:`Javascript` files within the ``js_source`` structure path is parsed
when the sphinx builder is initiated, and all relevant information is recorded
in the configuration environment, including the description for each element.

Each element description must use the :term:`reStructuredText` format and be
contained in docstrings in the form of:

.. code-block:: js

    /**
     * Return a temperature converted from Fahrenheit to Celsius.
     *
     * :param f: integer
     * :return: integer
     */
    function toCelsius(f) {
        return (5/9) * (f-32);
    }

The docstring should be placed immediately before the code being documented.
Each comment must start with a ``/**`` sequence in order to be recognized by the
:mod:`~champollion.parser`.

The docstring can also be in one line:

.. code-block:: js

    /** This is a description of the foo variable. */
    const foo = 42;

Using Directives
================

For all :term:`directives <Directive>`, only **one argument** must be given
which represent the ID of the element (class, function, etc...) which depends
on the file structure hierarchy.

If the path of a folder named *"example"* is given to the ``js_source``
configuration value, the ID of a class named **TestClass** included in the
file *"./example/module/test.js"* would be ``example.module.test.TestClass``
and would be documented as follow:

.. sourcecode:: rest

    *****************************
    example.module.test.TestClass
    *****************************

    .. js:autoclass:: example.module.test.TestClass

Champollion add all :term:`directives <Directive>` to the
`Javascript domain <http://www.sphinx-doc.org/en/stable/domains.html#the-javascript-domain>`_.

.. note::

    The ``js:`` prefix must be used for each directive, or the following line
    should be added to the `Sphinx configuration file
    <http://sphinx-doc.org/config.html>`_::

        # conf.py
        primary_domain = "js"

js:automodule
-------------

Document nested elements from a module represented by a *file* or a
**index.js** file within a folder::

    example/
     |- index.js
     `- test.js

Two modules are available in the example above: **example** and **example.test**

.. sourcecode:: rest

    .. js:automodule:: example


js:autodata
-----------

Document a variable declaration using one of the following way:

* `const <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/const>`_
* `let <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let>`_
* `var <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/var>`_

Example:

.. code-block:: js

    /** PI Mathematical Constant. */
    const PI = 3.14159265359;

.. sourcecode:: rest

    .. js:autodata:: example.PI

js:autofunction
---------------

Document a function declaration using one of the following way:

* `function <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function>`_
* `function expression <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/function>`_
* `arrow-type function <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions>`_
* `function* statement <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*>`_
* `function* expression <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/function*>`_

Example:

.. code-block:: js

    /**
     * Return a distance converted from Meter to Miles.
     *
     * :param d: integer
     * :return: integer
     */
    const toMiles = (d) => {
        return d * 0.00062137;
    }

.. sourcecode:: rest

    .. js:autofunction:: example.toMiles

.. warning::

    These function declaration statements are not supported at the moment:

    * `Function object <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function>`_
    * `GeneratorFunction object <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/GeneratorFunction>`_
    * `async function <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function>`_
    * `async function expression <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/async_function>`_

js:autoclass
------------

Document a class declaration using one of the following way:

* `class <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/class>`_
* `class expression <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/class>`_

Example:

.. code-block:: js

    /*
     * A Square class declaration.
     */
    class Square extends Polygon {

        /** Square ID. */
        static name = 'Square';

        /** Construct the Square object. */
        constructor(length) {
            super(length, length);
        }

        /**
         * Compute and get the area from the square.
         *
         * :return: double
         */
        get area() {
            return this.height * this.width;
        }

        /**
         * Indicate whether a polygon is a square.
         *
         * :param polygon: :class:`Polygon` object
         * :return: boolean
         */
        static isSquare(polygon) {
            return (polygon.height === polygon.width);
        }
    }

.. sourcecode:: rest

    .. js:autoclass:: example.Square

.. warning::

    The documentation of nested elements within a variable is not supported

    Example:

    .. code-block:: js

        var Rectangle = {
            constructor(height, width) {
                this.height = height;
                this.width = width;
            }
        };

js:automethod
-------------

Document a method using one of the following way:

* `getter <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get>`_
* `setter <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/set>`_
* `arrow-type method <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions>`_
* `static <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/static>`_

Example:

From the class example above, the static method `isSquare` would be documented
as follow:

.. sourcecode:: rest

    .. js:automethod:: example.Square.isSquare

.. warning::

    These method declaration statements are not supported at the moment:

    * `method generator <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*>`_
    * `async method <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function>`_


js:autoattribute
----------------

Document a class attribute using one of the following way:

* `static <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/static>`_

Example:

From the class example above, the static attribute `name` would be
documented as follow:

.. sourcecode:: rest

    .. js:autoattribute:: example.Square.name
