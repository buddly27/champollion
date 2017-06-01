# :coding: utf-8

from sphinx import addnodes

from .base import BaseDirective


class AutoDataDirective(BaseDirective):
    """Generate reStructuredText from JavaScript data.

    .. sourcecode:: rest

        .. js:autodata:: my-data-id

    """
    #: Javascript data are not callable
    has_arguments = False

    #: Define the Object type
    objtype = "data"

    def __init__(
        self, name, arguments, options, content, lineno, content_offset,
        block_text, state, state_machine
    ):
        """Initiate the directive.

        Raise an error if the variable id is unavailable within the Javascript
        environment parsed.

        """
        super(AutoDataDirective, self).__init__(
            name, arguments, options, content, lineno, content_offset,
            block_text, state, state_machine
        )
        self.content = self._generate_import_statement()
        self.content += self._generate_description()

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
        name = self._env["name"]
        value = self._env["value"]
        module_id = self._env["module_id"]
        variable_type = self._env["type"]
        module_name = self._module_env[module_id]["name"]

        node["type"] = "data"
        node["id"] = self._env["id"]
        node["module"] = module_name
        node['fullname'] = name

        node += addnodes.desc_type(variable_type + " ", variable_type + " ")
        node += addnodes.desc_addname(module_name + ".", module_name + ".")
        node += addnodes.desc_name(name, name)
        node += addnodes.desc_annotation(" = " + value, " = " + value)
        return name, module_name

    def get_index_text(self, objectname, name_obj):
        """Return relevant index text.
        """
        return " (global variable or constant)"
