# :coding: utf-8

from sphinx import addnodes
import docutils.parsers.rst.directives

from .base import BaseDirective


class AutoDataDirective(BaseDirective):
    """Directive to render :term:`Javascript` data documentation.

    The unique argument should be the identifier of the data element.

    .. sourcecode:: rest

        .. js:autodata:: module.DATA

    The available options are:

    * alias:
        String element to replace the data name.

    * module-alias:
        String element to replace the module name.

    * module-path-alias:
        String element to replace the module path.

    * force-partial-import:
        Indicate whether the data import statement display should be indicated
        with partial import if the data element is exported.

    * skip-value:
        Indicate whether data value should be skipped.

    .. seealso::

        :ref:`directive/autodata`

    """
    #: Javascript data are not callable
    has_arguments = False

    #: Define the Object type
    objtype = "data"

    #: data options
    option_spec = {
        "alias": docutils.parsers.rst.directives.unchanged_required,
        "module-alias": docutils.parsers.rst.directives.unchanged_required,
        "module-path-alias": docutils.parsers.rst.directives.unchanged_required,
        "force-partial-import": lambda x: True,
        "skip-value": lambda x: True,
    }

    def handle_signature(self, signature, node):
        """Update the signature *node*."""
        env = self.state.document.settings.env.element_environment
        module_env = self.state.document.settings.env.module_environment

        name = self.options.get("alias", env["name"])
        module_id = env["module_id"]
        module_name = self.options.get(
            "module-alias", module_env[module_id]["name"]
        )
        value = env["value"]
        variable_type = env["type"]

        skip_value = self.options.get("skip-value", False)

        node["type"] = "data"
        node["id"] = env["id"]
        node["module"] = module_name
        node["fullname"] = name

        node += addnodes.desc_type(variable_type + " ", variable_type + " ")
        node += addnodes.desc_addname(module_name + ".", module_name + ".")
        node += addnodes.desc_name(name, name)
        if not skip_value:
            node += addnodes.desc_annotation(" = " + value, " = " + value)

        return name, module_name

    def before_content(self):
        """Update the content.

        Compute the description and import statement if available.

        """
        env = self.state.document.settings.env.element_environment
        module_env = self.state.document.settings.env.module_environment

        self.content = self.generate_import_statement(
            env, module_env, self.options.get("force-partial-import")
        )
        self.content += self.generate_description(env)
