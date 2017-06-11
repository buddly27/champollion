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


.. _directive/autodata:

Using autodata
==============

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

    * `Function object <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function>`_
    * `GeneratorFunction object <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/GeneratorFunction>`_
    * `async function <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function>`_
    * `async function expression <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/async_function>`_

.. _directive/autoclass:

Using autoclass
===============

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

.. _directive/automethod:

Using automethod
================

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


.. _directive/autoattribute:

Using autoattribute
===================

Document a class attribute using one of the following way:

* `static <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/static>`_

Example:

From the class example above, the static attribute `name` would be
documented as follow:

.. sourcecode:: rest

    .. js:autoattribute:: example.Square.name
