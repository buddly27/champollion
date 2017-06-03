.. _introduction:

************
Introduction
************

Champollion is a :term:`Sphinx` extension which provides a way to parse
:term:`Javascript` source code and produce automatic API documentation.

The documentation must use the :term:`reStructuredText` format and be contained
in docstrings in the form of:

.. code-block:: js

    /**
     * Return a temperature converted from Fahrenheit to Celsius.
     *
     * .. seealso:: https://en.wikipedia.org/wiki/Celsius
     */
    function toCelsius(f) {
        return (5/9) * (f-32);
    }


The documentation generated will be as follow:

.. image:: /image/doc-example.png
   :alt: Documentation generated from function
   :scale: 50 %
