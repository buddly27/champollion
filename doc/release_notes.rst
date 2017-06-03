.. _release_notes:

*************
Release Notes
*************

.. release:: 0.1.0
    :date: 2017-06-03

    .. change:: new

        Added the following :term:`directives <Directive>`:

        * :class:`js:autodata <champollion.directive.data.AutoDataDirective>`
          to generate the documentation from a data id.
        * :class:`js:autofunction <champollion.directive.function.AutoFunctionDirective>`
          to generate the documentation from a function id.
        * :class:`js:autoclass <champollion.directive.class_.AutoClassDirective>`
          to generate the documentation from a class id.
        * :class:`js:automethod <champollion.directive.method.AutoMethodDirective>`
          to generate the documentation from a method id.
        * :class:`js:autoattribute <champollion.directive.attribute.AutoAttributeDirective>`
          to generate the documentation from a attribute id.

    .. change:: new

        Added :mod:`champollion.viewcode` to provide the source code for each
        :term:`Javascript` element documentation generated.

    .. change:: new

        Added :mod:`champollion.parser` to analyse :term:`Javascript` source
        code

    .. change:: new

        Initial release.
