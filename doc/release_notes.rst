.. _release_notes:

*************
Release Notes
*************

.. release:: 0.3.1
    :date: 2017-06-06

    .. change:: fixed
        :tags: javascript-parser

        Fix :func:`champollion.parser.data_parser.get_data_environment` to
        preserve the data value with all of its potential nested elements.

        Format the value on one line to ease the display.

    .. change:: fixed
        :tags: directive

        As an `arrow-type function <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions>`_
        can be also be considered as a variable, ensure that the
        :class:`js:automodule <champollion.directive.module_directive.AutoModuleDirective>`
        and :class:`js:autoclass <champollion.directive.class_directive.AutoClassDirective>`
        directives use the :class:`~champollion.directive.function_directive.AutoFunctionDirective`
        and :class:`~champollion.directive.method_directive.AutoMethodDirective`
        in priority when available.

.. release:: 0.3.0
    :date: 2017-06-05

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.module_directive.AutoModuleDirective`
        :term:`directive <Directive>` to generate the documentation from a module
        id representing a module (a file name without the '.js' extension or a
        directory with an 'index.js' file) parsed within the :term:`Javascript`
        source code.

    .. change:: new
        :tags: directive

        Added ``:members:`` option to the
        :class:`js:automodule <champollion.directive.module_directive.AutoModuleDirective>`
        directive to provide a way to document all or part of the members
        contained within a module.

    .. change:: new
        :tags: directive

        Added ``:undoc-members:`` option to the
        :class:`js:automodule <champollion.directive.module_directive.AutoModuleDirective>`
        directive to provide a way to document the module members without
        docstrings.

    .. change:: new
        :tags: directive

        Added ``:private-members:`` option to the
        :class:`js:automodule <champollion.directive.module_directive.AutoModuleDirective>`
        directive to provide a way to document the private module members.

    .. change:: new
        :tags: documentation

        Added :ref:`usage <using>` documentation.

    .. change:: fixed
        :tags: documentation

        Fix the zipball link in the :ref:`installation <installing>` documentation.

.. release:: 0.2.0
    :date: 2017-06-04

    .. change:: new
        :tags: directive

        Added ``:members:`` option to the
        :class:`js:autoclass <champollion.directive.class_directive.AutoClassDirective>`
        directive to provide a way to document all or part of the members
        contained within a class.

    .. change:: new
        :tags: directive

        Added ``:skip-constructor:`` option to the
        :class:`js:autoclass <champollion.directive.class_directive.AutoClassDirective>`
        directive to provide a way to filter a class constructor in the
        documentation generated.

    .. change:: new
        :tags: directive

        Added ``:undoc-members:`` option to the
        :class:`js:autoclass <champollion.directive.class_directive.AutoClassDirective>`
        directive to provide a way to document the class members without
        docstrings.

    .. change:: new
        :tags: directive

        Added ``:private-members:`` option to the
        :class:`js:autoclass <champollion.directive.class_directive.AutoClassDirective>`
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

        Added :class:`~champollion.directive.data_directive.AutoDataDirective`
        :term:`directive <Directive>` to generate the documentation from a data
        id representing a variable parsed within the :term:`Javascript` source
        code.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.function_directive.AutoFunctionDirective`
        :term:`directive <Directive>` to generate the documentation from a
        function id representing a function parsed within the :term:`Javascript`
        source code.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.class_directive.AutoClassDirective`
        :term:`directive <Directive>` to generate the documentation from a
        class id representing a class parsed within the :term:`Javascript`
        source code.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.method_directive.AutoMethodDirective`
        :term:`directive <Directive>` to generate the documentation from a
        method id representing a class method parsed within the
        :term:`Javascript` source code.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.attribute_directive.AutoAttributeDirective`
        :term:`directive <Directive>` to generate the documentation from an
        attribute id representing a class attribute parsed within the
        :term:`Javascript` source code.

    .. change:: new
        :tags: documentation

        Added :ref:`installation <installing>` documentation.
