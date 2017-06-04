.. _release_notes:

*************
Release Notes
*************

.. release:: 0.2.0
    :date: 2017-06-04

    .. change:: new
        :tags: directive

        Added ``:members:`` option to the
        :class:`js:autoclass <champollion.directive.class_.AutoClassDirective>`
        directive to provide a way to document all or part of the members
        contained within a class.

    .. change:: new
        :tags: directive

        Added ``:skip-constructor:`` option to the
        :class:`js:autoclass <champollion.directive.class_.AutoClassDirective>`
        directive to provide a way to filter a class constructor in the
        documentation generated.

    .. change:: new
        :tags: directive

        Added ``:undoc-members:`` option to the
        :class:`js:autoclass <champollion.directive.class_.AutoClassDirective>`
        directive to provide a way to document the class members without
        docstrings.

    .. change:: new
        :tags: directive

        Added ``:private-members:`` option to the
        :class:`js:autoclass <champollion.directive.class_.AutoClassDirective>`
        directive to provide a way to document the private class members.

    .. change:: new
        :tags: configuration

        Added ``js_class_options`` global configuration value which contains a
        list of class directive boolean option activated by default.

        .. code-block:: python

            js_class_options=['members', 'undoc-members']

.. release:: 0.1.0
    :date: 2017-06-03

    .. change:: new
        :tags: configuration

        Added ``js_source`` global configuration value which contains the path
        to the :term:`Javascript` source code to parse.

    .. change:: new
        :tags: javascript-parser

        Added :mod:`champollion.parser` to parse :term:`Javascript` source
        code.

    .. change:: new

        Added :mod:`champollion.viewcode` to provide html source code linked to
        each API documentation generated.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.data.AutoDataDirective`
        :term:`directive <Directive>` to generate the documentation from a data
        id representing a variable parsed within the :term:`Javascript` source
        code.

        .. sourcecode:: rest

            .. js:autodata:: example.DATA

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.function.AutoFunctionDirective`
        :term:`directive <Directive>` to generate the documentation from a
        function id representing a function parsed within the :term:`Javascript`
        source code.

        .. sourcecode:: rest

            .. js:autofunction:: example.doSomething

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.class_.AutoClassDirective`
        :term:`directive <Directive>` to generate the documentation from a
        class id representing a class parsed within the :term:`Javascript`
        source code.

        .. sourcecode:: rest

            .. js:autoclass:: example.AwesomeClass

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.method.AutoMethodDirective`
        :term:`directive <Directive>` to generate the documentation from a
        method id representing a class method parsed within the
        :term:`Javascript` source code.

        .. sourcecode:: rest

            .. js:automethod:: example.AwesomeClass.myMethod

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.attribute.AutoAttributeDirective`
        :term:`directive <Directive>` to generate the documentation from an
        attribute id representing a class attribute parsed within the
        :term:`Javascript` source code.

        .. sourcecode:: rest

            .. js:autoattribute:: example.AwesomeClass.myAttribute
