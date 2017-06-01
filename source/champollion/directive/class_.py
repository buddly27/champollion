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

    def __init__(
        self, name, arguments, options, content, lineno, content_offset,
        block_text, state, state_machine
    ):
        """Initiate the directive.
        """
        super(AutoClassDirective, self).__init__(
            name, arguments, options, content, lineno, content_offset,
            block_text, state, state_machine
        )
        self.content = self._generate_import_statement()
        self.content += self._generate_description()

        nested_elements = {}

        for attribute_environment in self._env["attribute"].values():
            line_number = attribute_environment["line_number"]
            nested_elements[line_number] = (
                "autoattribute", attribute_environment["id"]
            )

        for method_environment in self._env["method"].values():
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

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
        name = self._env["name"]
        module_id = self._env["module_id"]
        module_name = self._module_env[module_id]["name"]

        node["type"] = "class"
        node["id"] = self._env["id"]
        node["module"] = module_name
        node['fullname'] = name

        node += addnodes.desc_type("class ", "class ")
        node += addnodes.desc_addname(module_name + ".", module_name + ".")
        node += addnodes.desc_name(name, name)
        node += addnodes.desc_parameterlist()

        return name, module_name

    def before_content(self):
        """Do not keep track of the object and module in sub-module."""
        pass
