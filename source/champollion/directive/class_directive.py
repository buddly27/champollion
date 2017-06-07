# :coding: utf-8

from sphinx import addnodes
from docutils.statemachine import StringList

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
    }

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
        env = self.state.document.settings.env.element_environment
        module_env = self.state.document.settings.env.module_environment

        name = env["name"]
        module_id = env["module_id"]
        module_name = module_env[module_id]["name"]

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

        self.content = self._generate_import_statement(env, module_env)
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
        if not members:
            return

        nested_elements = {}

        # Gather class attributes
        for attribute_environment in env["attribute"].values():
            # As a method can also be a variable, use the method directive
            # by default when available
            if attribute_environment["id"] in env["method"].keys():
                continue

            name = attribute_environment["name"]
            description = attribute_environment["description"]
            if description is None and not undoc_members:
                continue

            if name.startswith("_") and not private_members:
                continue

            if members is True or name in members:
                line_number = attribute_environment["line_number"]
                nested_elements[line_number] = (
                    "autoattribute", attribute_environment["id"]
                )

        # Gather class methods
        for method_environment in env["method"].values():
            name = method_environment["name"]
            if name == "constructor" and skip_constructor:
                continue

            description = method_environment["description"]
            if description is None and not undoc_members:
                continue

            if name.startswith("_") and not private_members:
                continue

            if members is True or name in members:
                line_number = method_environment["line_number"]
                nested_elements[line_number] = (
                    "automethod", method_environment["id"]
                )

        # Add attributes and methods to content while respecting the line order
        for line_number in sorted(nested_elements.keys()):
            directive, element_id = nested_elements[line_number]
            element_rst = (
                "\n.. js:{directive}:: {id}\n\n".format(
                    directive=directive, id=element_id
                )
            )
            self.content += StringList(element_rst.split("\n"))
