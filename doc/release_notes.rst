.. _release_notes:

*************
Release Notes
*************

.. release:: 0.4.1
    :date: 2017-06-11

    .. change:: fixed

        Remove implicit relative imports within packages for compatibility
        with Python 3.

.. release:: 0.4.0
    :date: 2017-06-11

    .. change:: new
        :tags: javascript-parser

        Added :func:`champollion.parser.file_element.fetch_import_environment`
        to fetch elements imported from different modules if possible::

            import {element as alias} from "./module"
            import * from "./module"

    .. change:: new
        :tags: javascript-parser

        Added :func:`champollion.parser.file_element.fetch_export_environment`
        to fetch elements exported from different modules if possible::

            export {element as alias} from "./module"
            export * from "./module"

    .. change:: new
        :tags: javascript-parser

        Added :func:`champollion.parser.file_element.update_from_exported_elements`
        to regroup the exported element within a file environment if possible.

    .. change:: new
        :tags: directive

        Added ``:alias:`` options to all directives (except
        :class:`js:automodule <champollion.directive.module_element.AutoModuleDirective>`
        ) to modify the name of the element to display.

    .. change:: new
        :tags: directive

        Added ``:module-alias:`` options to all directives to modify the name
        of the module from the element to display.

    .. change:: new
        :tags: directive

        Added ``:force-partial-import:`` options to all directives to force
        the display of partial import if the element is exported. On the
        :class:`js:automodule <champollion.directive.module_element.AutoModuleDirective>`,
        this options is applied to all nested elements.

    .. change:: new
        :tags: javascript-parser

        Added more unit tests for :mod:`champollion.parser`

    .. change:: fixed
        :tags: javascript-parser

        Fixed :func:`class parser <champollion.parser.class_element.fetch_environment>`
        to recognize class expression assigned to **let** and **var** variables.

.. release:: 0.3.3
    :date: 2017-06-07

    .. change:: fixed
        :tags: javascript-parser

        Fixed unit tests for
        :func:`function parser <champollion.parser.function_element.fetch_environment>`

.. release:: 0.3.2
    :date: 2017-06-07

    .. change:: changed
        :tags: javascript-parser

        Added support for
        `function expression <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/function>`_
        in :func:`function parser <champollion.parser.function_element.fetch_environment>`.

    .. change:: changed
        :tags: javascript-parser, directive

        Added support for
        `function generator <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*>`_
        in :func:`function parser <champollion.parser.function_element.fetch_environment>`
        and :class:`~champollion.directive.function_element.AutoFunctionDirective`.

    .. change:: fixed
        :tags: javascript-parser

        Fixed :func:`function parser <champollion.parser.function_element.fetch_environment>`
        to recognize arrow-type function expression assigned to **let** and
        **var** variables.

    .. change:: fixed
        :tags: javascript-parser, directive

        Fixed :func:`function parser <champollion.parser.function_element.fetch_environment>`
        and :class:`~champollion.directive.function_element.AutoFunctionDirective`
        to support anonymous function.

    .. change:: changed
        :tags: documentation

        Update :ref:`usage <using>` documentation.

.. release:: 0.3.1
    :date: 2017-06-06

    .. change:: fixed
        :tags: javascript-parser

        Fix :func:`champollion.parser.data_element.fetch_environment` to
        preserve the data value with all of its potential nested elements.

        Format the value on one line to ease the display.

    .. change:: fixed
        :tags: directive

        As an `arrow-type function <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions>`_
        can be also be considered as a variable, ensure that the
        :class:`js:automodule <champollion.directive.module_element.AutoModuleDirective>`
        and :class:`js:autoclass <champollion.directive.class_element.AutoClassDirective>`
        directives use the :class:`~champollion.directive.function_element.AutoFunctionDirective`
        and :class:`~champollion.directive.class_element.AutoMethodDirective`
        in priority when available.

.. release:: 0.3.0
    :date: 2017-06-05

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.module_element.AutoModuleDirective`
        :term:`directive <Directive>` to generate the documentation from a module
        id representing a module (a file name without the '.js' extension or a
        directory with an 'index.js' file) parsed within the :term:`Javascript`
        source code.

    .. change:: new
        :tags: directive

        Added ``:undoc-members:`` option to the
        :class:`js:automodule <champollion.directive.module_element.AutoModuleDirective>`
        directive to provide a way to document the module members without
        docstrings.

    .. change:: new
        :tags: directive

        Added ``:private-members:`` option to the
        :class:`js:automodule <champollion.directive.module_element.AutoModuleDirective>`
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
        :class:`js:autoclass <champollion.directive.class_element.AutoClassDirective>`
        directive to provide a way to document all or part of the members
        contained within a class.

    .. change:: new
        :tags: directive

        Added ``:skip-constructor:`` option to the
        :class:`js:autoclass <champollion.directive.class_element.AutoClassDirective>`
        directive to provide a way to filter a class constructor in the
        documentation generated.

    .. change:: new
        :tags: directive

        Added ``:undoc-members:`` option to the
        :class:`js:autoclass <champollion.directive.class_element.AutoClassDirective>`
        directive to provide a way to document the class members without
        docstrings.

    .. change:: new
        :tags: directive

        Added ``:private-members:`` option to the
        :class:`js:autoclass <champollion.directive.class_element.AutoClassDirective>`
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

        Added :class:`~champollion.directive.data_element.AutoDataDirective`
        :term:`directive <Directive>` to generate the documentation from a data
        id representing a variable parsed within the :term:`Javascript` source
        code.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.function_element.AutoFunctionDirective`
        :term:`directive <Directive>` to generate the documentation from a
        function id representing a function parsed within the :term:`Javascript`
        source code.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.class_element.AutoClassDirective`
        :term:`directive <Directive>` to generate the documentation from a
        class id representing a class parsed within the :term:`Javascript`
        source code.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.class_element.AutoMethodDirective`
        :term:`directive <Directive>` to generate the documentation from a
        method id representing a class method parsed within the
        :term:`Javascript` source code.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.class_element.AutoAttributeDirective`
        :term:`directive <Directive>` to generate the documentation from an
        attribute id representing a class attribute parsed within the
        :term:`Javascript` source code.

    .. change:: new
        :tags: documentation

        Added :ref:`installation <installing>` documentation.
