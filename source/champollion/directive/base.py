# :coding: utf-8

from sphinx.domains.javascript import JSObject

from .rst_generator import rst_string


class BaseDirective(JSObject):
    """Base class for :term:`Javascript` object directive.
    """

    #: Only the object id argument is required
    required_arguments = 1

    #: No optional argument is available
    optional_arguments = 0

    #: Content is automatically generated and can not be manually entered
    has_content = False

    #: Nested element is automatically generated and can not be manually entered
    allow_nesting = False

    #: No prefix is displayed right before the documentation entry
    display_prefix = None

    def run(self):
        """Run the directive."""
        # The signature is always the first argument.
        signature = self.arguments[0]

        js_env = self.state.document.settings.env.app.config.js_environment
        if signature not in js_env[self.objtype].keys():
            raise self.error(
                "The {objtype} id is unavailable: {signature}".format(
                    objtype=self.objtype,
                    signature=signature
                )
            )

        env = js_env[self.objtype][signature]
        module_env = js_env["module"]

        # Update references
        ref_context = self.state.document.settings.env.ref_context
        ref_context["js:module"] = env["module_id"]

        # Update settings environment
        self.state.document.settings.env.element_environment = env
        self.state.document.settings.env.module_environment = module_env

        return super(BaseDirective, self).run()

    def generate_import_statement(
        self, environment, module_environment, force_partial_import=False
    ):
        """Return import statement generated from *environment* and
        *module_environment*.

        The import statement will be generated only if the element is exported
        and the usage of partial import will depend whether the element is
        exported as default.

        *force_partial_import* indicate whether the usage of partial import
        should be used even if the element is exported as default.

        .. warning::

            The statement is using :term:`Javascript` ES6
            :js:external:`import <Statements/import>` keyword

        Example:

        .. code-block:: js

            import element from "module"
            import {partialElement} from "module"

        """
        name = self.options.get("alias", environment["name"])
        module_id = environment["module_id"]
        module_path = self.options.get(
            "module-path-alias", module_environment[module_id]["path"]
        )
        exported = environment["exported"]
        is_default = environment["default"]

        if exported and is_default and not force_partial_import:
            return rst_string(
                "``import {name} from \"{module}\"``\n".format(
                    name=name, module=module_path
                )
            )

        if exported and (not is_default or force_partial_import):
            return rst_string(
                "``import {{{name}}} from \"{module}\"``\n".format(
                    name=name, module=module_path
                )
            )

        return rst_string()

    def generate_description(self, environment):
        """Return description generated from *environment*.
        """
        description = environment["description"]

        content = rst_string()
        if description:
            content += rst_string(description)

        return content
