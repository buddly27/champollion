# :coding: utf-8

from sphinx import addnodes

from .base import BaseDirective


class AutoFunctionDirective(BaseDirective):
    """Generate reStructuredText from JavaScript function.

    .. sourcecode:: rest

        .. js:autofunction:: my-function-id

    """
    #: Javascript function is callable
    has_arguments = True

    #: Define the Object type
    objtype = "function"

    def __init__(
        self, name, arguments, options, content, lineno, content_offset,
        block_text, state, state_machine
    ):
        """Initiate the directive.

        Raise an error if the variable id is unavailable within the Javascript
        environment parsed.

        """
        super(AutoFunctionDirective, self).__init__(
            name, arguments, options, content, lineno, content_offset,
            block_text, state, state_machine
        )
        self.content = self._generate_import_statement()
        self.content += self._generate_description()

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
        name = self._env["name"]
        module_id = self._env["module_id"]
        module_name = self._module_env[module_id]["name"]

        node["type"] = "function"
        node["id"] = self._env["id"]
        node["module"] = module_name
        node['fullname'] = name

        node += addnodes.desc_addname(module_name + ".", module_name + ".")
        node += addnodes.desc_name(name, name)

        param_list = addnodes.desc_parameterlist()
        for argument in self._env["arguments"]:
            param_list += addnodes.desc_parameter(argument, argument)
        node += param_list

        return name, module_name
