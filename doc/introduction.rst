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
     * :param f: integer
     * :return: integer
     */
    function toCelsius(f) {
        return (5/9) * (f-32);
    }


The documentation generated will be as follow (if using the `readthedocs
<https://pypi.python.org/pypi/sphinx_rtd_theme>`_ template):

.. image:: /image/doc-example.png
   :alt: Documentation generated from function
   :scale: 50 %

.. seealso::

    `Who is Champollion? <https://en.wikipedia.org/wiki/Jean-Fran%C3%A7ois_Champollion>`_
