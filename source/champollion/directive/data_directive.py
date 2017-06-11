# :coding: utf-8

from sphinx import addnodes
import docutils.parsers.rst.directives

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

    #: data options
    option_spec = {
        "alias": docutils.parsers.rst.directives.unchanged_required,
        "module-alias": docutils.parsers.rst.directives.unchanged_required,
        "force-partial-import": lambda x: True,
    }

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
        env = self.state.document.settings.env.element_environment
        module_env = self.state.document.settings.env.module_environment

        name = self.options.get("alias", env["name"])
        module_id = env["module_id"]
        module_name = self.options.get(
            "module-alias", module_env[module_id]["name"]
        )
        value = env["value"]
        variable_type = env["type"]

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

        self.content = self._generate_import_statement(
            env, module_env, self.options.get("force-partial-import")
        )
        self.content += self._generate_description(env)
