# :coding: utf-8

from sphinx import addnodes

from .base_directive import BaseDirective


class AutoDataDirective(BaseDirective):
    """Generate reStructuredText from JavaScript data.

    .. sourcecode:: rest

        .. js:autodata:: my-data-id

    """
    #: Javascript data are not callable
    has_arguments = False

    #: Define the Object type
    objtype = "data"

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
        env = self.state.document.settings.env.element_environment
        module_env = self.state.document.settings.env.module_environment

        name = env["name"]
        value = env["value"]
        module_id = env["module_id"]
        variable_type = env["type"]
        module_name = module_env[module_id]["name"]

        node["type"] = "data"
        node["id"] = env["id"]
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

    def before_content(self):
        """Compute the description.
        """
        env = self.state.document.settings.env.element_environment
        module_env = self.state.document.settings.env.module_environment

        self.content = self._generate_import_statement(env, module_env)
        self.content += self._generate_description(env)
