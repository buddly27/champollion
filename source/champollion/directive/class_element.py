# :coding: utf-8

import collections

from sphinx import addnodes
import docutils.parsers.rst.directives

from .base import BaseDirective

from .rst_generator import (
    get_rst_attribute_elements,
    get_rst_method_elements
)


def _parse_members(argument):
    """Convert the :members: options to class directive."""
    if argument is None:
        return True
    return [arg.strip() for arg in argument.split(",")]


class AutoClassDirective(BaseDirective):
    """Directive to render :term:`Javascript` class documentation.

    The unique argument should be the identifier of the class element.

    .. sourcecode:: rest

        .. js:autoclass:: module.AwesomeClass

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

    .. seealso::

        :ref:`directive/autoclass`

    """
    #: Javascript class is callable
    has_arguments = True

    #: Define the Object type
    objtype = "class"

    #: classes options
    option_spec = {
        "members": _parse_members,
        "skip-constructor": lambda x: True,
        "undoc-members": lambda x: True,
        "private-members": lambda x: True,
        "alias": docutils.parsers.rst.directives.unchanged_required,
        "module-alias": docutils.parsers.rst.directives.unchanged_required,
        "force-partial-import": lambda x: True,
    }

    def handle_signature(self, signature, node):
        """Update the signature *node*."""
        env = self.state.document.settings.env.element_environment
        module_env = self.state.document.settings.env.module_environment

        name = self.options.get("alias", env["name"])
        module_id = env["module_id"]
        module_name = self.options.get(
            "module-alias", module_env[module_id]["name"]
        )

        node["type"] = "class"
        node["id"] = env["id"]
        node["module"] = module_name
        node['fullname'] = name

        node += addnodes.desc_type("class ", "class ")
        node += addnodes.desc_addname(module_name + ".", module_name + ".")
        node += addnodes.desc_name(name, name)

        param_list = addnodes.desc_parameterlist()
        for method_environment in env["method"].values():
            if method_environment["name"] == "constructor":
                for argument in method_environment["arguments"]:
                    param_list += addnodes.desc_parameter(argument, argument)
        node += param_list

        return name, module_name

    def before_content(self):
        """Update the content.

        Compute the description and import statement if available, and generate
        the class nested directive elements to integrate to the content.

        """
        env = self.state.document.settings.env.element_environment
        module_env = self.state.document.settings.env.module_environment

        self.content = self.generate_import_statement(
            env, module_env, self.options.get("force-partial-import")
        )
        self.content += self.generate_description(env)

        # Automatic boolean options
        options = self.env.config.js_class_options

        # Options manually set
        skip_constructor = self.options.get(
            "skip-constructor", "skip-constructor" in options
        )
        undoc_members = self.options.get(
            "undoc-members", "undoc-members" in options
        )
        private_members = self.options.get(
            "private-members", "private-members" in options
        )

        members = self.options.get("members", "members" in options)
        if members:
            rst_elements = {}

            whitelist = (
                members if isinstance(members, collections.Iterable) else None
            )

            # Gather class attributes
            rst_elements = get_rst_attribute_elements(
                env,
                whitelist_names=whitelist,
                blacklist_ids=env["method"].keys(),
                undocumented_members=undoc_members,
                private_members=private_members,
                rst_elements=rst_elements
            )

            # Gather class methods
            rst_elements = get_rst_method_elements(
                env,
                whitelist_names=whitelist,
                skip_constructor=skip_constructor,
                undocumented_members=undoc_members,
                private_members=private_members,
                rst_elements=rst_elements,
            )

            # Add content while respecting the line order
            for line_number in sorted(rst_elements.keys()):
                for rst_element in rst_elements[line_number]:
                    self.content += rst_element


class AutoMethodDirective(BaseDirective):
    """Directive to render :term:`Javascript` class method documentation.

    The unique argument should be the identifier of the class method element.

    .. sourcecode:: rest

        .. js:automethod:: module.AwesomeClass.awesomeMethod

    .. seealso::

        :ref:`directive/automethod`

    """
    #: Javascript method is callable
    has_arguments = True

    #: Define the Object type
    objtype = "method"

    def handle_signature(self, signature, node):
        """Update the signature *node*."""
        env = self.state.document.settings.env.element_environment

        name = env["name"]
        prefix = env["prefix"]

        node["type"] = "method"
        node["id"] = env["id"]
        node['fullname'] = name

        if prefix is not None:
            node += addnodes.desc_type(prefix + " ", prefix + " ")
        node += addnodes.desc_name(name, name)

        param_list = addnodes.desc_parameterlist()
        for argument in env["arguments"]:
            param_list += addnodes.desc_parameter(argument, argument)
        node += param_list

        return name, None

    def before_content(self):
        """Update the content.

        Compute the description if available.

        """
        env = self.state.document.settings.env.element_environment

        self.content = self.generate_description(env)


class AutoAttributeDirective(BaseDirective):
    """Directive to render :term:`Javascript` class attribute documentation.

    The unique argument should be the identifier of the class attribute element.

    .. sourcecode:: rest

        .. js:autoattribute:: module.AwesomeClass.DATA

    .. seealso::

        :ref:`directive/autoattribute`

    """
    #: Javascript data are not callable
    has_arguments = False

    #: Define the Object type
    objtype = "attribute"

    def handle_signature(self, signature, node):
        """Update the signature *node*."""
        env = self.state.document.settings.env.element_environment

        name = env["name"]
        value = env["value"]
        prefix = env["prefix"]

        node["type"] = "attribute"
        node["id"] = env["id"]
        node['fullname'] = name

        if prefix is not None:
            node += addnodes.desc_type(prefix + " ", prefix + " ")
        node += addnodes.desc_name(name, name)
        node += addnodes.desc_annotation(" = " + value, " = " + value)
        return name, None

    def before_content(self):
        """Update the content.

        Compute the description if available.

        """
        env = self.state.document.settings.env.element_environment
        self.content = self.generate_description(env)
