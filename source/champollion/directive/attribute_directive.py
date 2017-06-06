# :coding: utf-8

from sphinx import addnodes

from .base_directive import BaseDirective


class AutoAttributeDirective(BaseDirective):
    """Generate reStructuredText from JavaScript data.

    .. sourcecode:: rest

        .. js:autoattribute:: my-attribute-id

    """
    #: Javascript data are not callable
    has_arguments = False

    #: Define the Object type
    objtype = "attribute"

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
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
        """Compute the description.
        """
        env = self.state.document.settings.env.element_environment

        self.content = self._generate_description(env)
