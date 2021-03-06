.. _release_notes:

*************
Release Notes
*************

.. release:: 1.0.0
    :date: 2020-05-31

    .. change:: new
        :tags: directive

        Updated :class:`js:automodule
        <champollion.directive.js_module.AutoModuleDirective>` to inherit from
        :class:`docutils.parsers.rst.Directive` instead of
        :class:`sphinx.directives.Directive` so it can work with Sphinx >= 1.8.

.. release:: 0.8.1
    :date: 2018-09-23

    .. change:: fixed

        Excluded the :term:`Sphinx` requirement version from 1.8 as `Directive`
        class is removed from the `sphinx.directives` module.

        .. seealso::

            `Sphinx Release 1.8.0
            <http://www.sphinx-doc.org/en/stable/changes.html#release-1-8-0-released-sep-13-2018>`_

.. release:: 0.8.0
    :date: 2018-07-14

    .. change:: new
        :tags: directive

        Added ``:skip-value:`` option to the
        :class:`js:autodata
        <champollion.directive.js_data.AutoDataDirective>` directive to
        prevent displayed the data value.

    .. change:: new
        :tags: directive

        Added ``:skip-value:`` option to the
        :class:`js:autoattribute
        <champollion.directive.js_class.AutoAttributeDirective>` directive to
        prevent displayed the attribute value.

    .. change:: new
        :tags: directive

        Added ``:skip-attribute-value:`` option to the
        :class:`js:autoclass
        <champollion.directive.js_class.AutoClassDirective>` directive to
        prevent displayed all attribute values within the class.

    .. change:: new
        :tags: directive

        Added ``:skip-attribute-value:`` option to the
        :class:`js:automodule
        <champollion.directive.js_module.AutoModuleDirective>` directive to
        prevent displayed all attribute values within the module.

    .. change:: new
        :tags: directive

        Added ``:skip-data-value:`` option to the
        :class:`js:automodule
        <champollion.directive.js_module.AutoModuleDirective>` directive to
        prevent displayed all data values within the module.

.. release:: 0.7.2
    :date: 2018-07-06

    .. change:: fixed

        Fixed package version issue.

.. release:: 0.7.1
    :date: 2018-07-06

    .. change:: fixed
        :tags: unit-tests

        Updated Travis configuration to run unit-tests for Python 3.6.

.. release:: 0.7.0
    :date: 2018-07-06

    .. change:: new
        :tags: configuration

        Added ``js_sources`` global configuration value which can contains
        several paths to :term:`Javascript` source codes to parse.

    .. change:: fixed
        :tags: javascript-parser

        Fixed :func:`champollion.parser.helper.get_docstring` to ensure that a
        docstring is not associated with an element when too many blank lines
        separate the docstring from the function.

.. release:: 0.6.0
    :date: 2017-07-03

    .. change:: new
        :tags: javascript-parser

        Added :func:`champollion.parser.js_file.fetch_file_description` to
        return description included in the docstring defined at the very
        beginning of the file.

    .. change:: changed
        :tags: javascript-parser

        Updated :func:`champollion.parser.js_file.fetch_environment` to include
        the file description in the environment.

    .. change:: new
        :tags: directive

        Updated :class:`js:automodule
        <champollion.directive.js_module.AutoModuleDirective>` to display the
        module description.

    .. change:: new
        :tags: directive

        Added ``:members:`` option to the
        :class:`js:automodule
        <champollion.directive.js_module.AutoModuleDirective>` directive to
        provide a way to document all or part of the members contained within a
        class.

        .. note::

            This option can be set automatically via the :ref:`js_module_options
            <configuration/js_module_options>` configuration

        .. warning::

            By default, only the description of the module will be displayed.

    .. change:: new
        :tags: directive

        Added ``:skip-description:`` option to the
        :class:`js:automodule
        <champollion.directive.js_module.AutoModuleDirective>` directive to
        provide a way to skip the module description.

        .. note::

            This option can be set automatically via the :ref:`js_module_options
            <configuration/js_module_options>` configuration

    .. change:: new
        :tags: javascript-parser

        Added module path to the module environment returned by
        :func:`champollion.parser.js_module.fetch_environment`

    .. change:: changed
        :tags: directive

        Updated all directives to use the module path when displaying the import
        statement::

            import {Element} from "example/module"

    .. change:: new
        :tags: directive

        Added ``:module-path-alias:`` options to all directives to modify the
        path of the module from the element to display.

    .. change:: fixed
        :tags: javascript-parser

        Updated the regular expression in the :mod:`data parser
        <champollion.parser.js_data.fetch_environment>` to recognize values
        spread over several lines::

            const DATA = {
                key1: 'value1',
                key2: 'value2',
                key3: 'value3',
            };

        .. warning::

            This update requires that **all** documented data statements end
            with a semi-colon.

    .. change:: fixed
        :tags: javascript-parser

        Updated the regular expression in the :mod:`attribute parser
        <champollion.parser.js_class.fetch_attribute_environment>` to recognize
        values spread over several lines::

            class AwesomeClass {
                static DATA = {
                    key1: 'value1',
                    key2: 'value2',
                    key3: 'value3',
                }
            }

        .. warning::

            This update requires that **all** documented attribute statements
            end with a semi-colon.

    .. change:: fixed
        :tags: javascript-parser

        Updated the regular expressions in the :mod:`method parser
        <champollion.parser.js_class.fetch_methods_environment>` to recognize
        arguments spread over several lines::

            class AwesomeClass {
                method(
                    argument1,
                    argument2,
                    argument3,
                ) {
                    console.log('Hello World')
                }
            }

.. release:: 0.5.2
    :date: 2017-06-29

    .. change:: fixed

        Updated the Sphinx dependency version to 1.6.2 as `module` and `method`
        directives where missing from the Javascript domain in older versions.

        .. seealso::

            `Sphinx Release Notes <https://github.com/sphinx-doc/sphinx/commit/3ba60ffd5dbd86ba3433db952304dcef6a3f023c>`_

    .. change:: changed

        Updated pytest dependency version to 3.0.0

.. release:: 0.5.1
    :date: 2017-06-25

    .. change:: fixed

        Added PyPi and RTD badges to the README page

.. release:: 0.5.0
    :date: 2017-06-25

    .. change:: new
        :tags: configuration

        Added ``js_module_options`` global configuration value which contains a
        list of class directive boolean option activated by default.

        .. code-block:: python

            js_module_options=['undoc-members', 'private-members']

    .. change:: new
        :tags: documentation

        Added :ref:`configuration <configuration>` documentation.

.. release:: 0.4.2
    :date: 2017-06-14

    .. change:: fixed
        :tags: directive

        Ensured that each element documented can be targeted by the standard
        `Javascript roles <http://www.sphinx-doc.org/en/stable/domains.html#the-javascript-domain>`_

    .. change:: changed
        :tags: javascript-parser

        Added ``js_environment`` global configuration value which will be
        filled automatically from the ``js_source`` global configuration via
        the :mod:`champollion.parser` if not provided.

        This ensure that the documentation is rebuilt when the source code is
        modified.

.. release:: 0.4.1
    :date: 2017-06-11

    .. change:: fixed

        Removed implicit relative imports within packages for compatibility
        with Python 3.

.. release:: 0.4.0
    :date: 2017-06-11

    .. change:: new
        :tags: javascript-parser

        Added :func:`champollion.parser.js_file.fetch_import_environment`
        to fetch elements imported from different modules if possible::

            import {element as alias} from "./module"
            import * from "./module"

    .. change:: new
        :tags: javascript-parser

        Added :func:`champollion.parser.js_file.fetch_export_environment`
        to fetch elements exported from different modules if possible::

            export {element as alias} from "./module"
            export * from "./module"

    .. change:: new
        :tags: javascript-parser

        Added :func:`champollion.parser.js_file.update_from_exported_elements`
        to regroup the exported element within a file environment if possible.

    .. change:: new
        :tags: directive

        Added ``:alias:`` options to all directives (except
        :class:`js:automodule <champollion.directive.js_module.AutoModuleDirective>`
        ) to modify the name of the element to display.

    .. change:: new
        :tags: directive

        Added ``:module-alias:`` options to all directives to modify the name
        of the module from the element to display.

    .. change:: new
        :tags: directive

        Added ``:force-partial-import:`` options to all directives to force
        the display of partial import if the element is exported. On the
        :class:`js:automodule <champollion.directive.js_module.AutoModuleDirective>`,
        this options is applied to all nested elements.

    .. change:: new
        :tags: javascript-parser

        Added more unit tests for :mod:`champollion.parser`

    .. change:: fixed
        :tags: javascript-parser

        Fixed :func:`class parser <champollion.parser.js_class.fetch_environment>`
        to recognize class expression assigned to **let** and **var** variables.

.. release:: 0.3.3
    :date: 2017-06-07

    .. change:: fixed
        :tags: javascript-parser

        Fixed unit tests for
        :func:`function parser <champollion.parser.js_function.fetch_environment>`

.. release:: 0.3.2
    :date: 2017-06-07

    .. change:: changed
        :tags: javascript-parser

        Added support for
        `function expression <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/function>`_
        in :func:`function parser <champollion.parser.js_function.fetch_environment>`.

    .. change:: changed
        :tags: javascript-parser, directive

        Added support for
        `function generator <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*>`_
        in :func:`function parser <champollion.parser.js_function.fetch_environment>`
        and :class:`~champollion.directive.js_function.AutoFunctionDirective`.

    .. change:: fixed
        :tags: javascript-parser

        Fixed :func:`function parser <champollion.parser.js_function.fetch_environment>`
        to recognize arrow-type function expression assigned to **let** and
        **var** variables.

    .. change:: fixed
        :tags: javascript-parser, directive

        Fixed :func:`function parser <champollion.parser.js_function.fetch_environment>`
        and :class:`~champollion.directive.js_function.AutoFunctionDirective`
        to support anonymous function.

    .. change:: changed
        :tags: documentation

        Update :ref:`usage <using>` documentation.

.. release:: 0.3.1
    :date: 2017-06-06

    .. change:: fixed
        :tags: javascript-parser

        Fix :func:`champollion.parser.js_data.fetch_environment` to
        preserve the data value with all of its potential nested elements.

        Format the value on one line to ease the display.

    .. change:: fixed
        :tags: directive

        As an `arrow-type function <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions>`_
        can be also be considered as a variable, ensure that the
        :class:`js:automodule <champollion.directive.js_module.AutoModuleDirective>`
        and :class:`js:autoclass <champollion.directive.js_class.AutoClassDirective>`
        directives use the :class:`~champollion.directive.js_function.AutoFunctionDirective`
        and :class:`~champollion.directive.js_class.AutoMethodDirective`
        in priority when available.

.. release:: 0.3.0
    :date: 2017-06-05

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.js_module.AutoModuleDirective`
        :term:`directive <Directive>` to generate the documentation from a module
        id representing a module (a file name without the '.js' extension or a
        directory with an 'index.js' file) parsed within the :term:`Javascript`
        source code.

    .. change:: new
        :tags: directive

        Added ``:undoc-members:`` option to the
        :class:`js:automodule <champollion.directive.js_module.AutoModuleDirective>`
        directive to provide a way to document the module members without
        docstrings.

    .. change:: new
        :tags: directive

        Added ``:private-members:`` option to the
        :class:`js:automodule <champollion.directive.js_module.AutoModuleDirective>`
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
        :class:`js:autoclass <champollion.directive.js_class.AutoClassDirective>`
        directive to provide a way to document all or part of the members
        contained within a class.

    .. change:: new
        :tags: directive

        Added ``:skip-constructor:`` option to the
        :class:`js:autoclass <champollion.directive.js_class.AutoClassDirective>`
        directive to provide a way to filter a class constructor in the
        documentation generated.

    .. change:: new
        :tags: directive

        Added ``:undoc-members:`` option to the
        :class:`js:autoclass <champollion.directive.js_class.AutoClassDirective>`
        directive to provide a way to document the class members without
        docstrings.

    .. change:: new
        :tags: directive

        Added ``:private-members:`` option to the
        :class:`js:autoclass <champollion.directive.js_class.AutoClassDirective>`
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

        Added :class:`~champollion.directive.js_data.AutoDataDirective`
        :term:`directive <Directive>` to generate the documentation from a data
        id representing a variable parsed within the :term:`Javascript` source
        code.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.js_function.AutoFunctionDirective`
        :term:`directive <Directive>` to generate the documentation from a
        function id representing a function parsed within the :term:`Javascript`
        source code.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.js_class.AutoClassDirective`
        :term:`directive <Directive>` to generate the documentation from a
        class id representing a class parsed within the :term:`Javascript`
        source code.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.js_class.AutoMethodDirective`
        :term:`directive <Directive>` to generate the documentation from a
        method id representing a class method parsed within the
        :term:`Javascript` source code.

    .. change:: new
        :tags: directive

        Added :class:`~champollion.directive.js_class.AutoAttributeDirective`
        :term:`directive <Directive>` to generate the documentation from an
        attribute id representing a class attribute parsed within the
        :term:`Javascript` source code.

    .. change:: new
        :tags: documentation

        Added :ref:`installation <installing>` documentation.
