# :coding: utf-8

from sphinx import addnodes
from docutils.statemachine import StringList

from .base import BaseDirective


class AutoClassDirective(BaseDirective):
    """Generate reStructuredText from JavaScript class.

    .. sourcecode:: rest

        .. js:autoclass:: my-class-id

    """
    #: Javascript class is callable
    has_arguments = True

    #: Define the Object type
    objtype = "class"

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
        node += addnodes.desc_parameterlist()

        return name, module_name

    def before_content(self):
        """Compute the description and nested element.
        """
        env = self.state.document.settings.env.element_environment
        module_env = self.state.document.settings.env.module_environment

        self.content = self._generate_import_statement(env, module_env)
        self.content += self._generate_description(env)

        nested_elements = {}

        for attribute_environment in env["attribute"].values():
            line_number = attribute_environment["line_number"]
            nested_elements[line_number] = (
                "autoattribute", attribute_environment["id"]
            )

        for method_environment in env["method"].values():
            line_number = method_environment["line_number"]
            nested_elements[line_number] = (
                "automethod", method_environment["id"]
            )

        for line_number in sorted(nested_elements.keys()):
            directive, element_id = nested_elements[line_number]
            element_rst = (
                "\n.. js:{directive}:: {id}\n\n".format(
                    directive=directive, id=element_id
                )
            )
            self.content += StringList(element_rst.split("\n"))
