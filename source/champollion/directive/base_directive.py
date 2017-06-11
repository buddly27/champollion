# :coding: utf-8

from sphinx.domains.javascript import JSObject

import rst_generator


class BaseDirective(JSObject):
    """Directive mixin to regroup common helper methods
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
        if not hasattr(self.state.document.settings.env, "js_environment"):
            raise self.error(
                "The javascript environment has not been parsed properly"
            )

        # The signature is always the first argument.
        signature = self.arguments[0]

        js_env = self.state.document.settings.env.js_environment
        if signature not in js_env[self.objtype].keys():
            raise self.error(
                "The {objtype} id is unavailable: {signature}".format(
                    objtype=self.objtype,
                    signature=signature
                )
            )

        self.state.document.settings.env.element_environment = (
            js_env[self.objtype][signature]
        )
        self.state.document.settings.env.module_environment = (
            js_env["module"]
        )

        return super(BaseDirective, self).run()

    def before_content(self):
        """Compute the description and nested element.
        """
        pass

    def _generate_import_statement(
        self, environment, module_environment, force_partial_import=False
    ):
        """Return the `StringList` import statement.
        """
        name = self.options.get("alias", environment["name"])
        module_id = environment["module_id"]
        module_name = self.options.get(
            "module-alias", module_environment[module_id]["name"]
        )
        exported = environment["exported"]
        is_default = environment["default"]

        if exported and is_default and not force_partial_import:
            return rst_generator.rst_string(
                "``import {name} from \"{module}\"``\n".format(
                    name=name, module=module_name
                )
            )

        if exported and (not is_default or force_partial_import):
            return rst_generator.rst_string(
                "``import {{{name}}} from \"{module}\"``\n".format(
                    name=name, module=module_name
                )
            )

        return rst_generator.rst_string()

    def _generate_description(self, environment):
        """Return the `StringList` description.
        """
        description = environment["description"]

        content = rst_generator.rst_string()
        if description:
            content += rst_generator.rst_string(description)

        return content
