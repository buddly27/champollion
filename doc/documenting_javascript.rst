.. _documenting_javascript:

**********************
Documenting Javascript
**********************

Contrarily to Python which has some high-level conventions for code
documentation (expressed in `PEP 257 <https://www.python.org/dev/peps/pep-0257/>`_),
there is no standard equivalent for the concept of docstrings in the
:term:`Javascript` world.

Champollion is using the same convention as `JSDoc <http://usejsdoc.org/>`_,
which define a docstring as a specific comment block starting with ``/**``:

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

The docstring can also be in one line:

.. code-block:: js

    /** This is a description of the foo variable. */
    const foo = 42;

Each element description must use the :term:`reStructuredText` language.

