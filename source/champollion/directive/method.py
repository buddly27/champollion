# :coding: utf-8

from sphinx import addnodes

from .base import BaseDirective


class AutoMethodDirective(BaseDirective):
    """Generate reStructuredText from JavaScript class.

    .. sourcecode:: rest

        .. js:automethod:: my-method-id

    """
    #: Javascript method is callable
    has_arguments = True

    #: Define the Object type
    objtype = "method"

    def __init__(
        self, name, arguments, options, content, lineno, content_offset,
        block_text, state, state_machine
    ):
        """Initiate the directive.

        Raise an error if the variable id is unavailable within the Javascript
        environment parsed.

        """
        super(AutoMethodDirective, self).__init__(
            name, arguments, options, content, lineno, content_offset,
            block_text, state, state_machine
        )
        self.content = self._generate_description()

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
        name = self._env["name"]
        prefix = self._env["prefix"]

        node["type"] = "method"
        node["id"] = self._env["id"]
        node['fullname'] = name

        if prefix is not None:
            node += addnodes.desc_type(prefix + " ", prefix + " ")
        node += addnodes.desc_name(name, name)

        param_list = addnodes.desc_parameterlist()
        for argument in self._env["arguments"]:
            param_list += addnodes.desc_parameter(argument, argument)
        node += param_list

        return name, None
