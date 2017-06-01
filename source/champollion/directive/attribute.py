# :coding: utf-8

from sphinx import addnodes

from .base import BaseDirective


class AutoAttributeDirective(BaseDirective):
    """Generate reStructuredText from JavaScript data.

    .. sourcecode:: rest

        .. js:autoattribute:: my-attribute-id

    """
    #: Javascript data are not callable
    has_arguments = False

    #: Define the Object type
    objtype = "attribute"

    def __init__(
        self, name, arguments, options, content, lineno, content_offset,
        block_text, state, state_machine
    ):
        """Initiate the directive.
        """
        super(AutoAttributeDirective, self).__init__(
            name, arguments, options, content, lineno, content_offset,
            block_text, state, state_machine
        )
        self.content = self._generate_description()

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
        name = self._env["name"]
        value = self._env["value"]
        prefix = self._env["prefix"]

        node["type"] = "attribute"
        node["id"] = self._env["id"]
        node['fullname'] = name

        if prefix is not None:
            node += addnodes.desc_type(prefix + " ", prefix + " ")
        node += addnodes.desc_name(name, name)
        node += addnodes.desc_annotation(" = " + value, " = " + value)
        return name, None
