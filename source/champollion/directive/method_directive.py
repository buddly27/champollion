# :coding: utf-8

from sphinx import addnodes

from .base_directive import BaseDirective


class AutoMethodDirective(BaseDirective):
    """Generate reStructuredText from JavaScript class.

    .. sourcecode:: rest

        .. js:automethod:: my-method-id

    """
    #: Javascript method is callable
    has_arguments = True

    #: Define the Object type
    objtype = "method"

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
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
        """Compute the description.
        """
        env = self.state.document.settings.env.element_environment

        self.content = self._generate_description(env)
