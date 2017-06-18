.. _directive:

****************
Using Directives
****************

.. _directive/automodule:

Using automodule
================

Document nested elements from a module represented by a *file* or a
**index.js** file within a folder::

    example/
     |- index.js
     `- test.js

Two modules are available in the example above: **example** and **example.test**

.. sourcecode:: rest

    .. js:automodule:: example

The available options are:

* undoc-members:
    Indicate whether members with no docstrings should be displayed.

* private-members:
    Indicate whether private members (with a name starting with an
    underscore) should be displayed.

* module-alias:
    String element to replace the module name.

* force-partial-import:
    Indicate whether each import statement display within the module
    should be indicated with partial import.

.. seealso::

    :ref:`configuration/js_module_options`

.. _directive/autodata:

Using autodata
==============

Document a variable declaration using one of the following way:

* :js:external:`const <Statements/const>`
* :js:external:`let <Statements/let>`
* :js:external:`var <Statements/var>`

Example:

.. code-block:: js

    /** PI Mathematical Constant. */
    const PI = 3.14159265359;

.. sourcecode:: rest

    .. js:autodata:: example.PI

The available options are:

* alias:
    String element to replace the data name.

* module-alias:
    String element to replace the module name.

* force-partial-import:
    Indicate whether the data import statement display should be indicated
    with partial import if the data element is exported.

.. _directive/autofunction:

Using autofunction
==================

Document a function declaration using one of the following way:

* :js:external:`function <Statements/function>`
* :js:external:`function expression <Operators/function>`
* :js:external:`arrow-type function <Functions/Arrow_functions>`
* :js:external:`function* statement <Statements/function*>`
* :js:external:`function* expression <Operators/function*>`

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

The available options are:

* alias:
    String element to replace the function name.

* module-alias:
    String element to replace the module name.

* force-partial-import:
    Indicate whether the function import statement display should be
    indicated with partial import if the function element is exported.

.. warning::

    These function declaration statements are not supported at the moment:

    * :js:external:`Function object <Global_Objects/Function>`
    * :js:external:`GeneratorFunction object <Global_Objects/GeneratorFunction>`
    * :js:external:`async function <Statements/async_function>`
    * :js:external:`async function expression <Operators/async_function>`

.. _directive/autoclass:

Using autoclass
===============

Document a class declaration using one of the following way:

* :js:external:`class <Statements/class>`
* :js:external:`class expression <Operators/class>`

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

The available options are:

* members:
    This option can be boolean if no arguments are given to indicate that
    all members should be documented, or a white list of member names to
    display.

* skip-constructor:
    Indicate whether the constructor method should be displayed if
    available.

* undoc-members:
    Indicate whether members with no docstrings should be displayed.

* private-members:
    Indicate whether private members (with a name starting with an
    underscore) should be displayed.

* alias:
    String element to replace the class name.

* module-alias:
    String element to replace the module name.

* force-partial-import:
    Indicate whether the class import statement display should be indicated
    with partial import if the class element is exported.

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

.. seealso::

    :ref:`configuration/js_class_options`

.. _directive/automethod:

Using automethod
================

Document a method using one of the following way:

* :js:external:`getter <Functions/get>`
* :js:external:`setter <Functions/set>`
* :js:external:`arrow-type method <Functions/Arrow_functions>`
* :js:external:`static <Classes/static>`

Example:

From the class example above, the static method `isSquare` would be documented
as follow:

.. sourcecode:: rest

    .. js:automethod:: example.Square.isSquare

.. warning::

    These method declaration statements are not supported at the moment:

    * :js:external:`method generator <Statements/function*>`
    * :js:external:`async method <Statements/async_function>`


.. _directive/autoattribute:

Using autoattribute
===================

Document a class attribute using one of the following way:

* :js:external:`static <Classes/static>`

Example:

From the class example above, the static attribute `name` would be
documented as follow:

.. sourcecode:: rest

    .. js:autoattribute:: example.Square.name
