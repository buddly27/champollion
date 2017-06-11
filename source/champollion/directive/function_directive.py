# :coding: utf-8

from sphinx import addnodes
import docutils.parsers.rst.directives

from .base_directive import BaseDirective


class AutoFunctionDirective(BaseDirective):
    """Generate reStructuredText from JavaScript function.

    .. sourcecode:: rest

        .. js:autofunction:: my-function-id

    """
    #: Javascript function is callable
    has_arguments = True

    #: Define the Object type
    objtype = "function"

    #: function options
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

        node["type"] = "function"
        node["id"] = env["id"]
        node["module"] = module_name
        node['fullname'] = name

        if env["generator"]:
            node += addnodes.desc_type("function* ", "function* ")

        if env["anonymous"]:
            node += addnodes.desc_name(name, name)
        else:
            node += addnodes.desc_addname(module_name + ".", module_name + ".")
            node += addnodes.desc_name(name, name)

        param_list = addnodes.desc_parameterlist()
        for argument in env["arguments"]:
            param_list += addnodes.desc_parameter(argument, argument)
        node += param_list

        return name, module_name

    def before_content(self):
        """Compute the description.
        """
        env = self.state.document.settings.env.element_environment
        module_env = self.state.document.settings.env.module_environment

        if not env["anonymous"]:
            self.content = self._generate_import_statement(
                env, module_env, self.options.get("force-partial-import")
            )

        self.content += self._generate_description(env)
