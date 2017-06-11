# :coding: utf-8

import collections

from sphinx import addnodes
import docutils.parsers.rst.directives

from champollion.renderer import RSTRenderer

from .base_directive import BaseDirective


def _parse_members(argument):
    """Convert the :members: options to class directive."""
    if argument is None:
        return True
    return [arg.strip() for arg in argument.split(",")]


class AutoClassDirective(BaseDirective):
    """Generate reStructuredText from JavaScript class.

    .. sourcecode:: rest

        .. js:autoclass:: my-class-id

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
        """Update the signature node.
        """
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
        """Compute the description and nested element.
        """
        env = self.state.document.settings.env.element_environment
        module_env = self.state.document.settings.env.module_environment

        self.content = self._generate_import_statement(
            env, module_env, self.options.get("force-partial-import")
        )
        self.content += self._generate_description(env)

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
            rst_elements = RSTRenderer.get_rst_attribute_elements(
                env,
                whitelist_names=whitelist,
                blacklist_ids=env["method"].keys(),
                undoc_members=undoc_members,
                private_members=private_members,
                rst_elements=rst_elements
            )

            # Gather class methods
            rst_elements = RSTRenderer.get_rst_method_elements(
                env,
                whitelist_names=whitelist,
                skip_constructor=skip_constructor,
                undoc_members=undoc_members,
                private_members=private_members,
                rst_elements=rst_elements,
            )

            # Add content while respecting the line order
            for line_number in sorted(rst_elements.keys()):
                for rst_element in rst_elements[line_number]:
                    self.content += rst_element
